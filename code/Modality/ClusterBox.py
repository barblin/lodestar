import numpy as np
import networkx as nx
from Modality.MergeKNN import MergePathsKNNResampled
from Modality.MergeGraph import MergeGraph
from NoiseRemoval.RemoveNoiseTransformed import remove_noise


class ClusterBoxResampled:
    """Create a box within the selected data set acting as a bufferzone to prevent abrupt density drops
    Modality computations are based on the KNNModalityResampled subclass -> resampled data & distances stored
    """
    def __init__(self, data, box_defining_dict):
        """
        :param box_defining_dict: Dictionary with features as keys and box "thickness" as value;
                                  e.g. {'X': 10, 'Y': 10, 'Z': 5}
        """
        self.data2cluster = data
        self.innerbox_boolarray = self.get_box_boolarray(box_defining_dict)
        self.innerbox2fulldata_dict = self.create_innerbox2fulldata_mapping()

    def get_box_boolarray(self, box_defining_dict):
        # Define empty bool array
        boolarr = np.zeros(self.data2cluster.shape[0], dtype=bool)
        # Loop through dictionary defining features and box thickness along given axis
        for axis, thickness in box_defining_dict.items():
            ax_vals = self.data2cluster[axis].values
            min_ax, max_ax = ax_vals.min(), ax_vals.max()
            # True -> is in border region between inner and outer box (then we reverse the boolarr)
            boolarr |= ax_vals < min_ax + thickness
            boolarr |= ax_vals > max_ax - thickness
        return ~boolarr

    def create_innerbox2fulldata_mapping(self):
        """Creates map from inner box indices (0,1,...,M) to full data.
        Store mapping in dictionary (needed for node remapping in graph):
            * key   ...inner box index
            * value ...full data index
        """
        full_data_idx = np.arange(self.data2cluster.shape[0])
        inner_data_idx = np.arange(np.sum(self.innerbox_boolarray))
        return dict(zip(inner_data_idx, full_data_idx[self.innerbox_boolarray]))

    def update_labels_large_box(self, G, lbls, msfull):
        """Map innerbox labels to full box labels"""
        # Relabels nodes in input graph
        G_relabeled = nx.relabel_nodes(G, self.innerbox2fulldata_dict, copy=True)
        # Relabel lbls (numpy array)
        lbls_relabeled = np.vectorize(self.innerbox2fulldata_dict.__getitem__)(lbls)
        # Relabel msfull (list of lists)
        msfull_relabeled = [[l[0], self.innerbox2fulldata_dict[l[1]], self.innerbox2fulldata_dict[l[2]]] for l in
                            msfull]
        return G_relabeled, lbls_relabeled, msfull_relabeled

    def build_morse_complex(self, data_full, density_obj, nb_neighbors,
                            nb_resampled_ds, step_size, velocity_scale, min_fraction_reject_h0, alpha,
                            knn_neighors_graph=30, beta=None):
        # Data to cluster within box
        cluster_data_innerbox = self.data2cluster.loc[self.innerbox_boolarray]

        # Compute rho
        rho = density_obj.knn_density(nb_neighbors)
        rho_innerbox = rho[self.innerbox_boolarray]

        # Morse complex/ascending manifold
        mer_gr = MergeGraph(k_neighbors=knn_neighors_graph, beta=beta)
        G, lbls, msfull = mer_gr.fit(cluster_data_innerbox.values, rho_innerbox)
        # Map innerbox labels to full box labels:
        G_rl, lbls_rl, msfull_rl = self.update_labels_large_box(G, lbls, msfull)

        # Provide a full set of labels to MergePathsKNNResampled (needed in GraphPreprocessing)
        lbls_full = -np.ones(self.data2cluster.shape[0], dtype=int)
        lbls_full[self.innerbox_boolarray] = lbls_rl

        mp = MergePathsKNNResampled(
            merge_sequence=msfull_rl,
            density=rho,
            labels=lbls_full,
            data_full=data_full,
            data_cluster=self.data2cluster,
            graph=G_rl,
            step_size=step_size,
            nb_neighbors=nb_neighbors,
            nb_resampled_ds=nb_resampled_ds,
            velocity_scale=velocity_scale,
            min_fraction_reject_h0=min_fraction_reject_h0
        )

        cldict, info_stats = mp.fit(alpha=alpha)
        flat_labels_innerbox = -np.ones(cluster_data_innerbox.shape[0], dtype=int)
        for i, modes in enumerate(cldict.values()):
            flat_labels_innerbox[np.isin(lbls_rl, modes)] = i
        # flat_labels_innerbox is clustering "only" inner box -> add outerbox indices
        final_cluster = -np.ones(self.data2cluster.shape[0], dtype=int)
        final_cluster[self.innerbox_boolarray] = flat_labels_innerbox

        return final_cluster, flat_labels_innerbox, G_rl, lbls_rl, rho, msfull_rl

    def remove_noise_box(self, full_data, clusters_box, rho, G, labels, adjacency_matrix,
                         pos_cols=['X', 'Y', 'Z'], nb_neigh_denstiy=10,
                         ra_col='ra', dec_col='dec', plx_col='parallax', pmra_col='pmra', pmdec_col='pmdec',
                         rv_col='dr2_radial_velocity', rv_err_col='dr2_radial_velocity_error', uvw_cols=['u', 'v', 'w'],
                         radius=8, isin_points=None, min_cluster_size=10, verbose=False):
        """Remove noise given the box constraints - points outside the inner box are considered noise"""
        # if no isin_points is provided we create own
        if isin_points is None:
            isin_points = np.ones(clusters_box.shape[0], dtype=bool)
        clustering_innerbox = -np.ones(np.sum(self.innerbox_boolarray))
        for uid in np.unique(clusters_box):
            if uid != -1:
                if verbose:
                    print(f'Modal region {uid} has {clusters_box[clusters_box == uid].size} members')

                if np.sum((clusters_box == uid) & isin_points) > 10:
                    ba, good_cluster = remove_noise(
                        data=self.data2cluster.loc[self.innerbox_boolarray].reset_index(drop=True),
                        cluster_bool_arr=clusters_box == uid,
                        G=G, labels=labels, density=rho[self.innerbox_boolarray],
                        pos_cols=pos_cols, nb_neigh_denstiy=nb_neigh_denstiy,
                        data_full=full_data.loc[self.innerbox_boolarray].reset_index(drop=True),
                        adjacency_mtrx=adjacency_matrix,
                        ra_col=ra_col, dec_col=dec_col, plx_col=plx_col, pmra_col=pmra_col, pmdec_col=pmdec_col,
                        rv_col=rv_col, rv_err_col=rv_err_col, uvw_cols=uvw_cols, radius=radius, isin_points=isin_points,
                        min_cluster_size=min_cluster_size, verbose=verbose
                    )
                    if good_cluster:
                        clustering_innerbox[ba] = uid
                        if verbose:
                            print(f'{np.sum(ba)} part of cluster')
                            print(f'{30 * "-"}')

        final_cluster = -np.ones(self.data2cluster.shape[0], dtype=int)
        final_cluster[self.innerbox_boolarray] = clustering_innerbox
        return final_cluster


