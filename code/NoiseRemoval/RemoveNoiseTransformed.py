import numpy as np
from scipy.optimize import minimize
import networkx as nx
from miscellaneous.utils import flatten_listlist
from scipy.sparse.csgraph import connected_components
from Modality.DensityEstKNN import DensityEstKNN
from NoiseRemoval.ClusterGMM import gmm_cut
from Graph.extract_neighbors import neighboring_modes
from Graph.GabrielGraph import gabriel_graph_adjacency
from NoiseRemoval.OptimalVelocity import optimize_velocity, transform_velocity, transform_velocity_diff


def remove_noise(data, cluster_bool_arr, G, pos_cols, labels, density, nb_neigh_denstiy,
                 data_full, ra_col, dec_col, plx_col, pmra_col, pmdec_col, rv_col, rv_err_col,
                 uvw_cols=None, radius=20
                 ):
    """Remove noise for a given cluster
    :param data: full data set
    :param cluster_bool_arr: bool array highlighting the cluster
    :param G: the MST graph describing the modes and their connection via saddle points
    :param pos_cols: poition columns (needed for combination of new feature space)
    :param labels: labels for each initial mode appearing in the data set
    :param density: point density estimate, usually via KNN density estimation
    :param nb_neigh_denstiy: number of neighbors to use for denstiy estimation
    """
    data_idx = np.arange(data.shape[0])
    # Get densest components in the given cluster
    _, cluster_labels, _ = gmm_cut(density[cluster_bool_arr], n_components=2)
    # get labels of local cluster mode containing the peak
    cluster_modes_dense = np.unique(labels[data_idx[cluster_bool_arr][cluster_labels]])
    # extract connected components from cluster_modes_dense (via G)
    nbs_saddle = np.array(flatten_listlist([list(int(n) for n in G.neighbors(cmd)) for cmd in cluster_modes_dense]))
    nodes_to_search = np.union1d(cluster_modes_dense, nbs_saddle)
    dense_subgraph = G.subgraph(nodes_to_search)
    largest_cc = np.array(list(max(nx.connected_components(dense_subgraph), key=len)), dtype=int)
    cluster_modes_dense = np.intersect1d(largest_cc, labels)

    # Get modes surrounding the dense cluster core
    nbs_modes = neighboring_modes(cluster_modes_dense, G, nb_neighbors=1)
    # Remove neighboring nodes that are not in the cluster
    nbs_modes = np.intersect1d(nbs_modes, np.unique(labels[cluster_bool_arr]))
    cut_filter = np.isin(labels, nbs_modes)  # filtered points: modal and surrounding regions
    rho_fitlered = density[cut_filter]  # get density of filtered points
    _, cluster_labels_filter, _ = gmm_cut(rho_fitlered, n_components=2)  # dense core points of this region
    cut_dense_core = data_idx[cut_filter][cluster_labels_filter]  # translate bool arr to data index

    # Compute gabriel graph of modal and surrounding regions
    ajm = gabriel_graph_adjacency(data.loc[cut_filter])

    # ---- Compute "optimal" cartesian velocity ----
    # Prepare data
    cols = [ra_col, dec_col, plx_col, pmra_col, pmdec_col, rv_col, rv_err_col]
    ra, dec, plx, pmra, pmdec, rv, rv_err = data_full.loc[cut_dense_core, cols].values.T
    # Prepare initial guess
    mean_uvw = np.zeros(3)
    if uvw_cols is not None:
        mean_uvw = np.mean(data_full.loc[cut_dense_core, uvw_cols], axis=0)
    # Compute optimal velocity
    sol = optimize_velocity(ra, dec, plx, pmra, pmdec, rv, rv_err, init_guess=mean_uvw, do_minimize=True)
    optimal_vel = sol.x
    # Compute propermotions under given optimal 3D velocity of full sample
    ra, dec, plx, pmra, pmdec, rv, rv_err = data_full.loc[
        cut_filter, [ra_col, dec_col, plx_col, pmra_col, pmdec_col, rv_col, rv_err_col]].values.T
    # Find best fitting rvs for given data
    # calculate rv for cases without rv estimations or very large errors
    idx_arr = np.arange(rv.size)
    rv_isnan_or_large_err = np.isnan(rv) | (np.abs(rv / rv_err) < 2)  # for large errors find better suited rvs
    list_op_rvs = []
    for i in idx_arr[rv_isnan_or_large_err]:
        opt_rv = minimize(fun=transform_velocity_diff, x0=0.,
                          args=(ra[i], dec[i], plx[i], pmra[i], pmdec[i], optimal_vel))
        list_op_rvs.append(opt_rv.x[0])
    # Set optimal rv's
    rv_computed = np.copy(rv)
    rv_computed[rv_isnan_or_large_err] = np.array(list_op_rvs)

    # Transform to uvw
    uvw_computed = transform_velocity(ra, dec, plx, pmra, pmdec, rv_computed)
    # only care about velocities near the optimal velocity -> others have too different space velocity
    uvw_calc_diff = np.linalg.norm(uvw_computed - optimal_vel, axis=1)
    # differences larger than radius (default=20) are very likely not part of stellar system
    cut_uvw_diff = uvw_calc_diff < radius

    # Prepare bool array for data
    data_idx = np.arange(data_full.shape[0])
    cluster_member_arr = np.zeros(data_full.shape[0], dtype=int)

    # Scale XYZ:
    # scales range from ~2-10 assuming the density in velocity is constant
    # while the space density can vary from a dense core to a less dense corona
    for scale in np.linspace(2, 10, 20):
        xyzuvw = np.c_[data_full.loc[cut_filter, pos_cols].values / scale, uvw_computed]
        # Compute densities
        duvw = DensityEstKNN(xyzuvw, nb_neigh_denstiy)
        rho_uvw = duvw.knn_density(nb_neigh_denstiy)
        # Predict membership via GMM with 2 components
        _, cut_gmm_xyzuvw, _ = gmm_cut(rho_uvw[cut_uvw_diff])
        # Extract connected component from dense component
        _, cc_idx = connected_components(ajm[cut_gmm_xyzuvw, :][:, cut_gmm_xyzuvw])
        # Combine CCs data points with originally defined dense core (to not miss out on potentially dropped points)
        cluster_indices = data_idx[cut_filter][cut_uvw_diff][cut_gmm_xyzuvw][cc_idx == np.argmax(np.bincount(cc_idx))]
        cluster_member_arr[cluster_indices] += 1

    return cluster_member_arr


def remove_noise_simple(data, cluster_bool_arr, G, labels, density):
    """Remove noise with only gmms"""
    data_idx = np.arange(data.shape[0])
    # Get densest components in the given cluster
    _, cluster_labels, _ = gmm_cut(density[cluster_bool_arr], n_components=2)
    # get labels of local cluster mode containing the peak
    cluster_modes_dense = np.unique(labels[data_idx[cluster_bool_arr][cluster_labels]])
    # extract connected components from cluster_modes_dense (via G)
    nbs_saddle = np.array(flatten_listlist([list(int(n) for n in G.neighbors(cmd)) for cmd in cluster_modes_dense]))
    nodes_to_search = np.union1d(cluster_modes_dense, nbs_saddle)
    dense_subgraph = G.subgraph(nodes_to_search)
    largest_cc = np.array(list(max(nx.connected_components(dense_subgraph), key=len)), dtype=int)
    cluster_modes_dense = np.intersect1d(largest_cc, labels)

    # Get modes surrounding the dense cluster core
    nbs_modes = neighboring_modes(cluster_modes_dense, G, nb_neighbors=2)
    # Remove neighboring nodes that are not in the cluster
    nbs_modes = np.intersect1d(nbs_modes, np.unique(labels[cluster_bool_arr]))
    cut_filter = np.isin(labels, nbs_modes)  # filtered points: modal and surrounding regions
    rho_fitlered = density[cut_filter]  # get density of filtered points
    _, cluster_labels_filter, _ = gmm_cut(rho_fitlered, n_components=2)  # dense core points of this region
    cut_dense_core = data_idx[cut_filter][cluster_labels_filter]  # translate bool arr to data index

    # Compute gabriel graph of modal and surrounding regions
    ajm = gabriel_graph_adjacency(data.loc[cut_filter])

    _, cc_idx = connected_components(ajm[cluster_labels_filter, :][:, cluster_labels_filter])
    # Combine CCs data points with originally defined dense core (to not miss out on potentially dropped points)
    cluster_indices = data_idx[cut_filter][cluster_labels_filter][cc_idx == np.argmax(np.bincount(cc_idx))]

    return np.isin(data_idx, cluster_indices)