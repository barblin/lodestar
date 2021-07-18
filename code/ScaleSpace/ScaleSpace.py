import numpy as np
from ScaleSpace.SparseMatrixOperations import JaccardMatrix

# potential transition values (from 1 cluster to the next one in 1 scale space step)
_DIRECT_LINK, _MERGE, _SPLIT = range(3)


class SingleMode:
    def __init__(self, cluster_id: int, level_id: int, index_arr: np.ndarray, mode: int):
        # unique cluster id -> matches scale_space_clusters key and retrieves this cluster
        self.cluster_id = cluster_id
        # scale space level id -> used for matching (clusters can only have parents in level_id-1)
        self.level_id = level_id
        # Cluster specific variables
        self.index_arr = index_arr  # index list of cluster members
        self.nb_points = index_arr.shape[0]  # number of cluster members
        self.mode = mode  # modal index
        # Connections to other clusters
        self.parent_list = []  # parent clusters (indices)
        self.child_list = []  # list of child clusters (each cluster can have multiple children)
        self.transition_signature = dict()

    def add_child(self, child):
        """Add child of cluster"""
        self.child_list.append(child)

    def add_parent(self, parent):
        """Add parent of cluster"""
        self.parent_list.append(parent)

    @staticmethod
    def intersection_np(a, b):
        """Fast way of evaluating intersection between numpy arrays"""
        return set(a.tolist()).intersection(set(b.tolist()))

    def both_modes_in_intersection(self, other_cluster) -> bool:
        """Tests if 2 clusters have both their modes in the intersection set"""
        intersection = self.intersection_np(self.index_arr, other_cluster.index_arr)
        # check if both modes are in the intersection
        return (self.mode in intersection) and (other_cluster.mode in intersection)

    def is_mode_in_other_cluster(self, other_cluster) -> bool:
        """Tests if currents cluster mode is contained in the other cluster"""
        return self.mode in other_cluster.index_arr

    def is_other_mode_in_here(self, other_cluster) -> bool:
        """Tests if the mode of another cluster has it's mode in this cluster"""
        return other_cluster.mode in self.index_arr

    def set_transition_signature(self, child_id: int, ts: int):
        """
        Setter for self.transition_signature. Possible values:
            * Direct link: modes of both clusters are in the intersection and Jaccard similarity is > 50%
            * Merge: Cluster mode is contained in the next one (but not necessarily vice versa)
            * Split: Part of a clusters breaks off and forms new cluster: Mode of next cluster is contained in a previous one
        For each child a different transition is possible (Direct link is only possible for one child)
        """
        self.transition_signature[child_id] = ts


class ScaleSpaceTree:
    """Organize entire hierachy of levels"""

    def __init__(self, data_size: int, min_jaccard_sim: float = 0.5):
        self.indices = np.arange(data_size, dtype=np.uint32)
        self.scale_space_clusters = dict()  # stores the clusters across the entire scale space
        self.curr_idx = 0  # helper variable which stores the current number of scale space clusters
        self.level_id = 0  # level id incrementer
        self.current_cluster_ids = None  # list of current clusters at the i'th scale space level
        self.min_jaccard_sim = min_jaccard_sim  # Store minimum jaccard similarity for direct link

    def init_new_partitioning(self, partitions: dict):
        """Store intial clusters in the current_clusters variable"""
        self.current_cluster_ids = list()
        for mode, cluster_members in partitions.items():
            cl = SingleMode(cluster_id=self.curr_idx, level_id=self.level_id, index_arr=np.array(cluster_members),
                            mode=mode)
            self.scale_space_clusters[self.curr_idx] = cl
            self.current_cluster_ids.append(self.curr_idx)  # Add cluster index info to current cluster list
            # increment cluster
            self.curr_idx += 1

    def labels_from_scale(self, n: int = -1) -> np.ndarray:
        """Returns for each data point a clustering corresponding to a certain scale"""
        level = np.max([c.level_id for c in self.scale_space_clusters.values()]) if n == -1 else n
        # instantiate labels array
        labels = np.full_like(self.indices, fill_value=-1, dtype=np.int64)
        for cl_id, cluster_obj in self.scale_space_clusters.items():
            if level == cluster_obj.level_id:
                # cluster_id is unique for each cluster collector
                labels[cluster_obj.index_arr] = cl_id
        return labels

    def next_scale(self, partitions: dict):
        # create current_clusters:
        self.init_new_partitioning(partitions)

        if self.level_id > 0:
            # There are already existing clusters -> match new to old ones
            # Create comparisons between existing clusters in cluster_collections
            # Comparison in sparse matrix: rows="new" clusters, cols="existing, scale-space" clusters

            # :::::::::: Clustering i'th level :::::::::::::
            # Represent current labels (clustering in i'th level) as single 1D array
            curr_labels = np.full_like(self.indices, fill_value=-1, dtype=np.int64)
            for clust_id in self.current_cluster_ids:
                # i'th labels corresponds to the i'th cluster in self.current_cluster_ids
                # -> important for indexing later
                curr_labels[self.scale_space_clusters[clust_id].index_arr] = clust_id
            # Store map to current labels in contingency matrix row
            unique_labels_current_scale = np.unique(curr_labels)

            # :::::::::: Clustering (i-1)'th level :::::::::::::
            # get the labels/cluster_ids from the previous iteration
            previous_labels = self.labels_from_scale(self.level_id - 1)
            # need a map from the integers to unique label id
            unique_labels_previous_scale = np.unique(previous_labels)

            # Compute jaccard similarity for each current cluster with each previous one
            # Instantiate jaccard matrix object: calculates jaccard similarity between each clustering
            # inherently sorts both input arrays by ascending value -> unique arrs map to orignal ids
            jm = JaccardMatrix(curr_labels, previous_labels)

            # Get all non zero values:
            # these are the entries where a cluster of level i-1 has a match to a cluster in the i'th level
            # row = cluster in level i   |   column = clusters in level i-1
            row_col_val_info = jm.nonzero_idx_pairs()
            # Set different linkage strategies
            self._set_linkage(row_col_val_info, unique_labels_previous_scale, unique_labels_current_scale)
        # increment the level
        self.level_id += 1
        return

    def _set_linkage(self, row_col_val_info, unique_labels_previous_scale, unique_labels_current_scale):
        """Calculate linkage between scale space clusters
        Merging clusters from level i-1 (=columns) to a cluster in level i (rows)
        """
        # sort by columns, then by descending jaccard sim value (sort bz second key important for direct link)
        colsorted_jacinfo = sorted(row_col_val_info, key=lambda item: (item['col'], item['val']))
        # Loop through level i-1 and look for clusters with large enough jaccard index and
        skip_col = -1  # skip rows where we have already found a match!
        for info in colsorted_jacinfo:
            # Test modal behaviour between two clusters
            ps = unique_labels_previous_scale[info['col']]
            cs = unique_labels_current_scale[info['row']]

            # We don't want to track the noise
            if ps != -1 and cs != -1:

                prev_level_cluster = self.scale_space_clusters[ps]
                curr_level_cluster = self.scale_space_clusters[cs]

                has_direct_link = False
                has_merged = False
                # Split has least priority, then merge, direct link is the most important one
                # :::: DIRECT LINK ::::
                # Test only for direct link condition if we don't already have match for that i-1 level cluster
                if skip_col != info['col']:
                    if info['val'] >= self.min_jaccard_sim:  # minimum jaccard distance requirement
                        if prev_level_cluster.both_modes_in_intersection(
                                curr_level_cluster):  # are both modes in the same intersection
                            # Add current cluster as child of prev_level_cluster
                            prev_level_cluster.add_child(curr_level_cluster.cluster_id)
                            curr_level_cluster.add_parent(prev_level_cluster.cluster_id)
                            # Save direct link transition
                            prev_level_cluster.set_transition_signature(child_id=curr_level_cluster.cluster_id,
                                                                        ts=_DIRECT_LINK)
                            # set skip column to that one (for direct link calculation)
                            skip_col = info['col']
                            has_direct_link = True
                # :::: MERGE condition ::::
                if not has_direct_link:
                    if prev_level_cluster.is_mode_in_other_cluster(curr_level_cluster):
                        # Add current cluster as child of prev_level_cluster
                        prev_level_cluster.add_child(curr_level_cluster.cluster_id)
                        curr_level_cluster.add_parent(prev_level_cluster.cluster_id)
                        prev_level_cluster.set_transition_signature(child_id=curr_level_cluster.cluster_id, ts=_MERGE)
                        # Set has_merged to True
                        has_merged = True
                # :::: SPLIT condition ::::
                if (not has_direct_link) and (not has_merged):
                    # In case there is neither a merging condition nor a direct link, we test for a split condition
                    if prev_level_cluster.is_other_mode_in_here(curr_level_cluster):
                        prev_level_cluster.add_child(curr_level_cluster.cluster_id)
                        curr_level_cluster.add_parent(prev_level_cluster.cluster_id)
                        prev_level_cluster.set_transition_signature(child_id=curr_level_cluster.cluster_id, ts=_SPLIT)

        return

