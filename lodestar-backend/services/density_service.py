import time
from threading import Thread

import numpy as np
from sklearn.neighbors import NearestNeighbors

from core.Modality.DensityEstKNN import DensityEstKNN
from core.NoiseRemoval.RemoveNoiseTransformed import remove_noise_tomatoext
from core.ScaleSpace.ScaleSpace import ScaleSpaceTree
from sklearn.neighbors import kneighbors_graph

from services.data.level_source import store_for_level


def density(df_cluster):
    return DensityEstKNN(df_cluster.values, max_neighbors=200)


def calc_max_dist(df_cluster, kwargs):
    nn = NearestNeighbors(n_jobs=-1).fit(df_cluster.values)
    dist, _ = nn.kneighbors(n_neighbors=kwargs['knn_density'],
                            return_distance=True)
    return np.median(np.percentile(dist, q=90, axis=1))


def scale_space_dense_components(data, te, columns, df_cluster):
    sst = ScaleSpaceTree(data_size=data.shape[0], min_jaccard_sim=0.5)

    alpha = 0.01
    data_idx = np.arange(data.shape[0])
    knn_densities_ssp = np.arange(10, 100, 2)

    for i, nb_neighs in enumerate(knn_densities_ssp):
        st = time.time()
        print(f'Number of neighbors: {nb_neighs}', end=' ')

        te.update(nb_neighs)
        res = te.fit(alpha=alpha)

        modes = {uid: data_idx[res == uid][np.argmax(te.t.weights_[res == uid])] for uid in np.unique(res)}
        part = {modes[uid]: data_idx[res == uid] for uid in np.unique(res)}
        sst.next_scale(partitions=part)
        print(f'- level {i} took {time.time() - st:.2f} sec')

        __produce_cluster_df(df_cluster, data, res, te, columns, i, modes)

    return sst


def __produce_cluster_df(df_cluster, data, res, te, columns, level, modes):
    ajm_knn = kneighbors_graph(df_cluster, n_neighbors=10, include_self=True, n_jobs=-1)
    clustering_res = -np.ones(data.shape[0])

    for uid in np.unique(res):
        print(f'Removing noise from cluster {uid}')
        ba, good_cluster = remove_noise_tomatoext(
            data=df_cluster,
            cluster_bool_arr=res == uid,
            te_obj=te,
            pos_cols=columns[:3],
            nb_neigh_denstiy=10,
            data_full=data,
            ra_col='ra', dec_col='dec', plx_col='parallax', pmra_col='pmra', pmdec_col='pmdec',
            rv_col='dr2_radial_velocity', rv_err_col='dr2_radial_velocity_error', uvw_cols=['u', 'v', 'w'],
            adjacency_mtrx=ajm_knn,
            radius=8,
            min_cluster_size=10
        )
        if good_cluster:
            clustering_res[ba] = modes[uid]
            print(f'{np.sum(ba)} part of cluster')
            print(f'{30 * "-"}')

    tb_stored = data[columns]
    tb_stored['labels'] = clustering_res
    store_for_level(tb_stored, str(level))
