import numpy as np
import networkx as nx
import copy
from code.Modality.kde_modality import KdeModality
from code.miscellaneous.utils import pairwise_loop


def np_intersection(a, b):
    return np.array(list(set(a.tolist()).intersection(b.tolist())))


def set_np(arr):
    return set(arr.tolist())


class MergePaths(KdeModality):
    """Implements the merge strategy evaluating
        1. the paths to be tested
        2. the modality of those paths
    """
    def __init__(self, data, graph, merge_sequence, density, labels, max_dist=None, nb_neighbors=None):
        super().__init__(data=data, max_dist=max_dist, nb_neighbors=nb_neighbors)
        self.graph = graph
        self.merge_sequence = merge_sequence
        self.density = density
        self.labels = labels
        self.clusters = dict()
        self.cannot_merge = list()

    def update_graph(self, new_graph, new_merge_sequence, labels, density):
        self.graph = new_graph
        self.merge_sequence = new_merge_sequence
        self.labels = labels
        self.density = density

    def paths2test(self, cluster2merge_1, cluster2merge_2):
        """Determine which additional tests between which peaks should be performed before we merge
        If two clusters would be merged by another cluster (outer cluster) then, perform the following additional dip tests
            1. From one peak to the next -> determine maximum of both clusters and get dip test from peak 2 peak
               (could save that result somewhere in case we would have to do it again for other clusters)
            2. From connecting strech between the two clusters, i.e. the peaks already in both clusters that are the closest to each other.
               This is a subset from the peak 2 peak path where the first peak is part of the first cluster and the path end is a peak part of the second clsuter
        """
        # For each cluster get peak with maximal density
        cl_1_maxdens = self.clusters[cluster2merge_1][np.argmax(self.density[np.array(self.clusters[cluster2merge_1])])]
        cl_2_maxdens = self.clusters[cluster2merge_2][np.argmax(self.density[np.array(self.clusters[cluster2merge_2])])]
        # Get path from peak to peak
        sh_path_peak2peak = np.array(nx.shortest_path(self.graph, cl_1_maxdens, cl_2_maxdens), dtype=int)
        # Peaks might be far apart so we also test path between nearest peaks that belong to either cluster
        #  1. Get first and last element in sh_path_peak2peak list that belong to a cluster
        cl_1_firstlast = np.where(np.isin(sh_path_peak2peak, self.clusters[cluster2merge_1]))[0][[0, -1]]
        cl_2_firstlast = np.where(np.isin(sh_path_peak2peak, self.clusters[cluster2merge_2]))[0][[0, -1]]
        #  2. the two middle indices are the ones where the clusters stop and then start again:
        index_start, index_stop = np.sort(np.concatenate([cl_1_firstlast, cl_2_firstlast]).ravel())[[1, 2]]
        return sh_path_peak2peak, sh_path_peak2peak[index_start:index_stop + 1]

    @staticmethod
    def is_dont_merge(arr, dont_merge):
        return set([arr[0], arr[-1]]) == set([dont_merge[0], dont_merge[-1]])

    def add_half_dontmerge(self, split_path):
        """Add the beginning of the cannot_merge path to the end of the normal path"""
        if len(split_path) > 1:
            final_path_list = []
            for i, (plo, phi) in enumerate(pairwise_loop(split_path)):
                plo_isdm = any([self.is_dont_merge(plo, cm) for cm in self.cannot_merge])
                phi_isdm = any([self.is_dont_merge(phi, cm) for cm in self.cannot_merge])
                nb_isdm = np.sum(np.array([plo_isdm, phi_isdm], dtype=np.uint))

                # ---- Cases ----
                # 1) No dip path
                if nb_isdm == 0:
                    final_path_list.append(np.array(plo))
                    if i == len(split_path) - 2:
                        final_path_list.append(np.array(phi))

                # 2) One dip in path
                elif nb_isdm == 1:
                    if plo_isdm:
                        split_path[i + 1] = np.insert(split_path[i + 1], 0, plo[-1])
                        if i == 0:
                            final_path_list.append(np.array([plo[0]]))
                        if i == len(split_path) - 2:
                            final_path_list.append(np.insert(phi, 0, plo[-1]))
                    if phi_isdm:
                        final_path_list.append(np.append(plo, phi[0]))
                        if i == len(split_path) - 2:
                            final_path_list.append(np.array([phi[-1]]))
                # 3) Adjacent paths both show significant dip
                elif nb_isdm == 2:
                    if i == 0:
                        final_path_list.append(np.array([plo[0]]))

                    final_path_list.append(np.array([plo[-1], phi[0]]))

                    if i == len(split_path) - 2:
                        final_path_list.append(np.array([phi[-1]]))
        else:
            final_path_list = []
            for sp in split_path:
                if any([self.is_dont_merge(sp, cm) for cm in self.cannot_merge]):
                    final_path_list.append(np.array([sp[0]]))
                    final_path_list.append(np.array([sp[-1]]))
                else:
                    final_path_list.append(sp)
        return final_path_list

    def cut_path(self, path):
        """Function that ends a path before a path would undergo a potion with a significant dip"""
        break_positions = []
        # check if the path is
        for dont_merge in self.cannot_merge:
            # If the part that cannot merge is fully contained in the path, then cut the path
            # If only a sub-portion of the cannot-merge part is in the path, we don't cross the "forbidden" trail
            if set_np(dont_merge).intersection(set_np(path)) == set_np(dont_merge) and (dont_merge.size > 0):
                f, l = np.where(np.isin(path, dont_merge))[0]
                break_positions.extend([f, l + 1])
        if len(break_positions) == 0:
            return [path]
        else:
            return self.add_half_dontmerge([arr for arr in np.split(path, np.sort(break_positions)) if arr.size > 0])

    def merge_simple(self, cluster_key_inner, new_path):
        """Inner cluster is fully contained in outer cluster which passes merge tests
        In this case merge outer cluster with inner and
            1. Add new peak indices from outer to inner list
            2. Remove outer key from dictionary
        return: updated cluster_dict"
        """
        # Union of both sets
        union = set(self.clusters[cluster_key_inner]).union(set(new_path))
        # set inner cluster to new combined cluster
        self.clusters[cluster_key_inner] = list(union)
        return

    def merge_clusters(self, new_path, cluster_key_inner_1, cluster_key_inner_2):
        """Merge two inner clusters that are contained in the outer cluster. Both clusters are merged into the cluster_key_1
        """
        # union of all three sets
        union = set(self.clusters[cluster_key_inner_1]).union(set(new_path), set(self.clusters[cluster_key_inner_2]))
        # set inner cluster to new combined cluster
        self.clusters[cluster_key_inner_1] = list(union)
        # remove later added cluster of the 2 existing from cluster_dict
        _ = self.clusters.pop(cluster_key_inner_2)
        return

    def cannot_merge_transition(self, path, alpha):
        """Find region in path that cannot merge"""
        path_max = path[np.isin(path, self.labels)]  # path containing only modes
        dont_merge = np.full(len(path_max), fill_value=-1)
        for clid, cl_path in self.clusters.items():
            dont_merge[np.isin(path_max, cl_path)] = clid
        # Don't merge these portions
        dm = np.concatenate([path_max[:-1][np.diff(dont_merge) != 0], path_max[1:][np.diff(dont_merge) != 0]])
        # In case there are more than 2 clusters in the sample --> at least 3 partitions that cannot merge
        if dm.size > 2:
            dm = []
            u, ind = np.unique(dont_merge, return_index=True)
            for xy in pairwise_loop(u[np.argsort(ind)]):
                p = path_max[np.isin(dont_merge, xy)]
                merge_path = self.test_multimodality(p, alpha)
                if not merge_path:
                    dm_i = np.concatenate([p[:-1][np.diff(dont_merge[np.isin(dont_merge, xy)]) != 0],
                                           p[1:][np.diff(dont_merge[np.isin(dont_merge, xy)]) != 0]])
                    dm.append(dm_i)

            return dm
        else:
            return [dm]

    def is_path_contained(self, path):
        for cluster_modes in self.clusters.values():
            if set_np(path).intersection(set(cluster_modes)) == set_np(path):
                return True
        return False

    def new_cannot_merge(self, path, alpha):
        cm_list = self.cannot_merge_transition(path=path, alpha=alpha)
        is_new_cm = True
        for cm in cm_list:
            if (len(cm) > 0) and (
                    not any([set_np(cm) == set_np(elem) for elem in self.cannot_merge])):
                self.cannot_merge.append(cm)
                is_new_cm = True
        return is_new_cm

    def merge_paths(self, alpha):
        # real clusters stores peaks of clusters that are merged together
        self.clusters = dict()
        self.cannot_merge = list()  # list of lists of peaks that cannot merge into a single cluster
        significant_dip_path = list()
        i = 0
        while i < len(self.merge_sequence):
            _, start, stop = self.merge_sequence[i]
            sh_path = np.array(nx.shortest_path(self.graph, start, stop), dtype=int)

            # If path crosses already "forbidden" route we cut it at that point
            path_list = self.cut_path(path=sh_path)

            for sh_path in path_list:
                # Is path already contained in one of the clusters: are the modes already contained
                if not self.is_path_contained(path=np_intersection(sh_path, self.labels)):
                    # If path contains more than 1 mode
                    if np_intersection(sh_path, self.labels).size > 1:
                        # Check for multimodality
                        do_merge_peaks, density_data = self.test_multimodality(sh_path=sh_path, alpha=alpha)
                        # If we shouldn't merge these peaks
                        if not do_merge_peaks:
                            significant_dip_path.append({'path': sh_path.tolist(), 'density_data': density_data})
                            if self.new_cannot_merge(path=sh_path, alpha=alpha):
                                # consider same track again & now splitting it according to cannot_merge list
                                i -= 1

                        # Merge two peaks
                        else:
                            intersection_keys = list()  # Clusters that share a common peak with the new path
                            # Post processing if existing clusters are merged
                            for key, existing_cl in self.clusters.items():
                                # Intersection between "new" cluster and old cluster
                                if len(set(existing_cl).intersection(set_np(sh_path))) > 0:
                                    intersection_keys.append(key)

                            if len(intersection_keys) == 0:
                                self.clusters[i] = sh_path.tolist()

                            # Merge strategies
                            if len(intersection_keys) == 1:
                                # The new cluster only shares
                                self.merge_simple(cluster_key_inner=intersection_keys[0], new_path=sh_path.tolist())
                            elif len(intersection_keys) == 2:
                                p_peak2peak, p_cluster_connection = self.paths2test(
                                    cluster2merge_1=intersection_keys[0],
                                    cluster2merge_2=intersection_keys[1],
                                )
                                do_merge_p1, do_merge_p2 = True, True

                                # We also check if the paths are not already contained in a cluster and thus deemed "mergable"
                                ppp_lbls = np_intersection(p_peak2peak, self.labels)
                                pcc_lbls = np_intersection(p_cluster_connection, self.labels)

                                if (pcc_lbls.size > 1) and (not self.is_path_contained(path=pcc_lbls)):
                                    do_merge_p1, density_data_p1 = self.test_multimodality(sh_path=p_cluster_connection, alpha=alpha)
                                if (ppp_lbls.size > 1) and (not self.is_path_contained(path=ppp_lbls)):
                                    do_merge_p2, density_data_p2 = self.test_multimodality(sh_path=p_peak2peak, alpha=alpha)
                                if do_merge_p1 and do_merge_p2:
                                    self.merge_clusters(new_path=sh_path.tolist(),
                                                        cluster_key_inner_1=intersection_keys[0],
                                                        cluster_key_inner_2=intersection_keys[1]
                                                        )
                                else:
                                    already_reduced = False
                                    if not do_merge_p1:
                                        significant_dip_path.append(
                                            {
                                                'path': p_cluster_connection.tolist(),
                                                'density_data': density_data_p1
                                            }
                                        )
                                        significant_dip_path.append(p_cluster_connection.tolist())
                                        if self.new_cannot_merge(path=p_cluster_connection, alpha=alpha):
                                            already_reduced = True
                                            i -= 1
                                    if not do_merge_p2:
                                        significant_dip_path.append(
                                            {
                                                'path': p_peak2peak.tolist(),
                                                'density_data': density_data_p2
                                            }
                                        )
                                        if self.new_cannot_merge(path=p_peak2peak, alpha=alpha) and (not already_reduced):
                                            i -= 1

                            elif len(intersection_keys) > 2:
                                raise ValueError(f'>2 intersection keys: {intersection_keys} path: {sh_path.tolist()}')

                    # In case the cluster only consists of 1 point, we add it here to the cluster list
                    elif np_intersection(sh_path, self.labels).size == 1:
                        self.clusters[i] = sh_path.tolist()
            # increment counter by one = next path
            i += 1
        return significant_dip_path

    def fit(self, alpha):
        """Merge paths +post-processing and return significantly dipped paths"""
        sig_dip_paths = self.merge_paths(alpha)
        # Post processing: Merge clusters via cannot merge rule
        break_graph_on_nodes = []   # break graphs on these saddle nodes
        for cm in self.cannot_merge:
            sh_path = np.array(nx.shortest_path(self.graph, *cm), dtype=int)
            saddle_pt_set = set(sh_path) - set(cm)
            break_graph_on_nodes.append(saddle_pt_set.pop())  # pop retrieves int item in set
        Gsplit = copy.deepcopy(self.graph)  # graph that we split on the given break nodes
        Gsplit.remove_nodes_from(break_graph_on_nodes)
        self.clusters = {i: [int(c) for c in cc] for i, cc in enumerate(nx.connected_components(Gsplit))}
        return sig_dip_paths, self.clusters

    def flat_clustering(self):
        flat_labels = np.full(self.data.shape[0], fill_value=-1)
        for i, modes in enumerate(self.clusters.values()):
            flat_labels[np.isin(self.labels, modes)] = i
        return flat_labels



