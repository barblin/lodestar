import time

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import kneighbors_graph

from core.Modality.DensityEstKNN import DensityEstKNN
from core.NoiseRemoval.RemoveNoiseTransformed import remove_noise_tomatoext
from core.ScaleSpace.ScaleSpace import ScaleSpaceTree
from services.data.level_source import store_for_level
from services.graph.tomato_ext_service import create_graph


def density(df_cluster):
    return DensityEstKNN(df_cluster.values, max_neighbors=200)


def calc_max_dist(df_cluster, kwargs):
    nn = NearestNeighbors(n_jobs=-1).fit(df_cluster.values)
    dist, _ = nn.kneighbors(n_neighbors=kwargs['knn_density'],
                            return_distance=True)
    return np.median(np.percentile(dist, q=90, axis=1))


def scale_space_dense_components(data, columns, df_cluster, alpha):
    sst = ScaleSpaceTree(data_size=data.shape[0], min_jaccard_sim=0.5)
    knn_densities_ssp = np.arange(10, 100, 2)

    res, te = create_graph(df_cluster, alpha)

    for i, nb_neighs in enumerate(knn_densities_ssp):
        st = time.time()
        print(f'Number of neighbors: {nb_neighs}', end=' ')

        res = te.fit(alpha=alpha)
        te.update(nb_neighs)

        tb_stored = __for_alpha(sst, df_cluster, data, te, columns, res)
        store_for_level(tb_stored, str(i), alpha)
        print(f'- level {i} took {time.time() - st:.2f} sec')

    return sst


def __for_alpha(sst, df_cluster, data, te, columns, res):
    data_idx = np.arange(data.shape[0])

    modes = {uid: data_idx[res == uid][np.argmax(te.t.weights_[res == uid])] for
             uid in np.unique(res)}
    part = {modes[uid]: data_idx[res == uid] for uid in np.unique(res)}
    sst.next_scale(partitions=part)

    return __for_res(df_cluster, data, res, te, columns, modes)


def __for_res(df_cluster, data, res, te, columns, modes):
    ajm_knn = kneighbors_graph(df_cluster, n_neighbors=10, include_self=True,
                               n_jobs=-1)
    clustering_res = -np.ones(data.shape[0])

    for uid in np.unique(res):
        ba, good_cluster = remove_noise_tomatoext(
            data=df_cluster,
            cluster_bool_arr=res == uid,
            te_obj=te,
            pos_cols=columns[:3],
            nb_neigh_denstiy=10,
            data_full=data,
            ra_col=columns[0], dec_col=columns[1], plx_col=columns[2],
            pmra_col=columns[3], pmdec_col=columns[4],
            rv_col=columns[5], rv_err_col=columns[6],
            uvw_cols=columns[3:6],
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
    return tb_stored
