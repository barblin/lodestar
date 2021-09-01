import numpy as np

from code.Modality.DensityEstKNN import DensityEstKNN
from code.Modality.MergeGraph import MergeGraph
from code.Modality.merge_strategy import MergePaths
from code.NoiseRemoval.RemoveNoiseTransformed import remove_noise_simple
from code.ScaleSpace.ScaleSpace import ScaleSpaceTree
from sklearn.neighbors import NearestNeighbors, KernelDensity


def density(df_cluster):
    return DensityEstKNN(df_cluster.values, max_neighbors=200)


def calc_max_dist(df_cluster, kwargs):
    nn = NearestNeighbors(n_jobs=-1).fit(df_cluster.values)
    dist, _ = nn.kneighbors(n_neighbors=kwargs['knn_density'],
                            return_distance=True)
    return np.median(np.percentile(dist, q=90, axis=1))


def remove_nosie(fc, df_cluster, G, lbls, rho, data_idx):
    modes_final = {}
    for uid in np.unique(fc):
        ba = remove_noise_simple(data=df_cluster, cluster_bool_arr=fc == uid, G=G,
                                 labels=lbls, density=rho)
        clidx = data_idx[ba]
        mode_idx = clidx[np.argmax(rho[clidx])]
        modes_final[mode_idx] = {'index': clidx, 'boolarr': ba}
    return modes_final


def merge_paths(df_cluster, G, msfull, rho, lbls, max_dist, kwargs, nb_neighs):
    # Merge paths
    mp = MergePaths(data=df_cluster, graph=G, merge_sequence=msfull,
                    density=rho, labels=lbls, max_dist=max_dist)
    sig_dip, cldict = mp.fit(alpha=kwargs['alpha'])
    fc = mp.flat_clustering()
    print(f'{np.unique(fc).size} cluster found with {nb_neighs} nn density')
    return fc


def scale_space_dense_components(X, df_cluster):
    de = density(df_cluster)
    data_idx = np.arange(X.shape[0])
    sst = ScaleSpaceTree(data_size=X.shape[0], min_jaccard_sim=0.5)

    knn_densities_ssp = [30, 50, 70, 90, 110, 130]

    for nb_neighs in knn_densities_ssp:
        kwargs = {'knn_density': nb_neighs, 'knn_neighors_graph': 30, 'alpha': 0.05}

        max_dist = calc_max_dist(df_cluster, kwargs)

        rho = de.knn_density(kwargs['knn_density'])
        # kde = KernelDensity(bandwidth=max_dist/2, atol=1e-6, rtol=1e-5).fit(df_cluster.values)
        # rho = np.exp(kde.score_samples(df_cluster.values)

        # Morse complex/ascending manifold
        mer_gr = MergeGraph(kwargs['knn_neighors_graph'])
        G, lbls, msfull = mer_gr.fit(df_cluster.values, rho)

        fc = merge_paths(df_cluster, G, msfull, rho, lbls, max_dist, kwargs, nb_neighs)

        # Remove noise
        modes_final = remove_nosie(fc, df_cluster, G, lbls, rho, data_idx)
        # add partition to the scale space
        part = {key: value['index'] for key, value in modes_final.items()}
        sst.next_scale(partitions=part)

    return sst
