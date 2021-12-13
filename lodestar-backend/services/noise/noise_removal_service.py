import numpy as np
from sklearn.neighbors import kneighbors_graph

from core.NoiseRemoval.RemoveNoiseTransformed import remove_noise_tomatoext


def remove_noise(df, df_cluster, res, te, columns):
    ajm_knn = kneighbors_graph(df_cluster, n_neighbors=10, include_self=True, n_jobs=-1)
    clustering_res = -np.ones(df.shape[0])

    for uid in np.unique(res):
        print(f'Removing noise from cluster {uid}')
        ba, good_cluster = remove_noise_tomatoext(
            data=df_cluster,
            cluster_bool_arr=res == uid,
            te_obj=te,
            pos_cols=columns[:3],
            nb_neigh_denstiy=10,
            data_full=df,
            ra_col='ra', dec_col='dec', plx_col='parallax', pmra_col='pmra', pmdec_col='pmdec',
            rv_col='dr2_radial_velocity', rv_err_col='dr2_radial_velocity_error', uvw_cols=['u', 'v', 'w'],
            adjacency_mtrx=ajm_knn,
            radius=8,
            min_cluster_size=10
        )
        if good_cluster:
            clustering_res[ba] = uid
            print(f'{np.sum(ba)} part of cluster')
            print(f'{30 * "-"}')
