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


def remove_noise_tomatoext(data, cluster_bool_arr, te_obj,
                           pos_cols, nb_neigh_denstiy,
                           data_full, ra_col, dec_col, plx_col, pmra_col, pmdec_col, rv_col, rv_err_col,
                           adjacency_mtrx, uvw_cols=None, radius=8, verbose=False, min_cluster_size=10
                           ):
    # ----- Part-I: extract dense core -------
    data_idx = np.arange(data.shape[0])
    # Get densest components in the given cluster
    _, cluster_labels, _, is_good_clustering = gmm_cut(te_obj.t.weights_[cluster_bool_arr], n_components=2)
    if not is_good_clustering:
        return None, False
    # get labels of local cluster mode containing the peak
    cluster_modes_dense = np.unique(te_obj.t.leaf_labels_[data_idx[cluster_bool_arr][cluster_labels]])
    # Add neighbors of densest region that is in the cluster:
    search_for_peak = cluster_modes_dense
    for dense_cl in cluster_modes_dense:
        peak_neighbors = np.intersect1d(te_obj.t.leaf_labels_[cluster_bool_arr],
                                        te_obj.cluster_borders[dense_cl].nonzero())
        search_for_peak = np.union1d(search_for_peak, peak_neighbors)
    # Get dense component of peak
    cut_dense_neighs = np.isin(te_obj.t.leaf_labels_, search_for_peak)  # filtered points: modal and surrounding regions
    _, cluster_labels_filter, _, is_good_clustering = gmm_cut(te_obj.t.weights_[cut_dense_neighs],
                                                              n_components=2)  # dense core points of this region
    if not is_good_clustering:
        return None, False
    # Dense core points
    cut_dense_core = data_idx[cut_dense_neighs][cluster_labels_filter]  # translate bool arr to data index
    if cut_dense_core.size < min_cluster_size:
        return None, False

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
        cut_dense_neighs, [ra_col, dec_col, plx_col, pmra_col, pmdec_col, rv_col, rv_err_col]].values.T
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

    # Prepare bool array for data
    cluster_member_arr = np.zeros(data_full.shape[0], dtype=int)

    # Transform to uvw
    uvw_computed = transform_velocity(ra, dec, plx, pmra, pmdec, rv_computed)
    # only care about velocities near the optimal velocity -> others have too different space velocity
    uvw_calc_diff = np.linalg.norm(uvw_computed - optimal_vel, axis=1)
    # differences larger than radius (default=20) are very likely not part of stellar system
    cut_uvw_diff = uvw_calc_diff < radius
    if np.sum(cut_uvw_diff) < min_cluster_size:
        # if only very few stars are found that share the same velocity, focus on the dense core
        return np.isin(data_idx, data_idx[cut_dense_neighs][cut_uvw_diff]), False
    if verbose:
        print(f':: 3rd filter step: {np.sum(cut_uvw_diff)} in proximity to optimal velocity')

    # Scale XYZ:
    # scales range from ~2-10 assuming the density in velocity is constant
    # while the space density can vary from a dense core to a less dense corona
    for scale in np.linspace(2, 10, 20):
        xyzuvw = np.c_[data_full.loc[cut_dense_neighs, pos_cols].values / scale, uvw_computed]
        # Compute densities
        duvw = DensityEstKNN(xyzuvw, nb_neigh_denstiy)
        rho_uvw = duvw.knn_density(nb_neigh_denstiy)
        # Predict membership via GMM with 2 components
        _, cut_gmm_xyzuvw, _, is_good_clustering = gmm_cut(rho_uvw[cut_uvw_diff], n_components=2)
        if not is_good_clustering:
            return None, False

            # Extract connected component from dense component
        _, cc_idx = connected_components(
            adjacency_mtrx[cut_dense_neighs, :][:, cut_dense_neighs][cut_uvw_diff, :][:, cut_uvw_diff][cut_gmm_xyzuvw,
            :][:,
            cut_gmm_xyzuvw])
        # Combine CCs data points with originally defined dense core (to not miss out on potentially dropped points)
        cluster_indices = data_idx[cut_dense_neighs][cut_uvw_diff][cut_gmm_xyzuvw][
            cc_idx == np.argmax(np.bincount(cc_idx))]
        cluster_member_arr[cluster_indices] += 1

    final_clustering_strict = cluster_member_arr >= 15  # More than 75% of hits
    if np.sum(final_clustering_strict) >= min_cluster_size:
        # Keep connected components
        _, cc_idx = connected_components(adjacency_mtrx[final_clustering_strict, :][:, final_clustering_strict])
        # Combine CCs data points with originally defined dense core (to not miss out on potentially dropped points)
        cluster_indices = data_idx[final_clustering_strict][cc_idx == np.argmax(np.bincount(cc_idx))]
        cluster_final_xyzuvw = np.isin(data_idx, cluster_indices)
        return cluster_final_xyzuvw, True
    else:
        return final_clustering_strict, False


