import numpy as np
from scipy.stats import norm
from sklearn.neighbors import kneighbors_graph
from core.Graph.GraphKdTreeBase import ClusterPreparation
from core.Modality.DensityEstKNN import DensityEstKNN
from sklearn.preprocessing import LabelEncoder


def uf_find(i, parents):
    """
    Find function for Union-Find data structure.

    Parameters:
        i (int): ID of point for which parent is required.
        parents (numpy array of shape (num_points)): array storing parents of each point.
    """
    if parents[i] == i:
        return i
    else:
        return uf_find(parents[i], parents)


def uf_union(i, j, parents, f):
    """
    Union function for Union-Find data structure. Peak of smaller function value is attached to peak of larger function value.

    Parameters:
        i (int): ID of first point to be merged.
        j (int): ID of second point to be merged.
        parents (numpy array of shape (num_points)): array storing parents of each point.
        f (numpy array of shape (num_points)): array storing function values of each point.
    """
    if f[i] > f[j]:
        parents[j] = i
    else:
        parents[i] = j


class InitialModes(DensityEstKNN):
    def __init__(self, data, max_neighbors):
        super().__init__(X=data.values, max_neighbors=max_neighbors)
        self.weights_ = None
        self.n_leaves_ = None
        self.leaf_labels_ = None

    def fit(self, knn):
        A = kneighbors_graph(self.data, n_neighbors=knn, include_self=False, mode='distance')
        num_pts = self.data.shape[0]
        # Calculate density
        self.weights_ = self.knn_density(knn)
        parents = -np.ones(num_pts, dtype=np.int32)
        # Prepare density: sort indices by density
        sorted_idxs = np.flip(np.argsort(self.weights_))
        inv_sorted_idxs = np.arange(num_pts)  # Mapping from index to density rank; lower index -> higher density
        for i in range(num_pts):
            inv_sorted_idxs[sorted_idxs[i]] = i
        # Graph which keeps the edge and node information: important for connected components function
        # Start Mode finding
        for i in range(num_pts):
            current_pt = sorted_idxs[i]  # loop through points in decreasing density fashion
            neighbors = A.indices[A.indptr[current_pt]:A.indptr[current_pt + 1]]
            # Neighbors with higher density:
            higher_neighbors = [n for n in neighbors if inv_sorted_idxs[n] <= i]
            if len(higher_neighbors)==0:
                # point is new peak
                parents[current_pt] = current_pt  # in this case, a point is it's own parent
            else:  # if a point has neighbors with higher densities
                # attribute point to neighbor with highest density
                g = higher_neighbors[np.argmax(self.weights_[np.array(higher_neighbors)])]  # highest density neighbor
                pg = uf_find(g, parents)  # parent = respective modal point of cluster
                parents[current_pt] = pg  # add mode point to points info

        labels = np.array([uf_find(n, parents) for n in range(num_pts)])
        self.leaf_labels_ = LabelEncoder().fit_transform(labels)
        self.n_leaves_ = np.max(self.leaf_labels_)+1
        return


class TomatoExtension(ClusterPreparation):
    def __init__(self, data, max_neighbors, beta, knn_cluster_graph, knn_hypotest, knn_max=100):
        super().__init__(data=data, max_neighbors=max_neighbors, beta=beta, knn=knn_hypotest)
        self.cluster_borders = None
        self.t = InitialModes(data, knn_max)
        self.t.fit(knn=knn_cluster_graph)

    def update(self, knn_hypotest, knn_cluster_graph=None):
        # Update distances to k'th neighbor + mid point dists
        self.update_kdtree(knn_hypotest)
        if knn_cluster_graph is not None:
            self.t.fit(knn=knn_cluster_graph)

    def compute_pvalue_simple(self, d_max, d_saddle):
        k = self.knn
        p = self.data.shape[-1]
        SB_alpha = p * np.sqrt(k / 2) * (np.log(d_saddle) - np.log(d_max))
        return 1 - norm.cdf(SB_alpha)

    def dist_saddle_maxmean(self, ba_cluster_base, ba_cluster_to_merge):
        dummy_c1, dummy_c2 = self.A[ba_cluster_base, :][:, ba_cluster_to_merge].nonzero()
        pts_c1 = np.arange(self.A.shape[0])[ba_cluster_base][dummy_c1]
        pts_c2 = np.arange(self.A.shape[0])[ba_cluster_to_merge][dummy_c2]
        edges = np.vstack([pts_c1, pts_c2]).T
        # Get midpoints of saddle edges
        midpoints = self.A[pts_c1, pts_c2]
        saddle_edges = edges[np.argmin(midpoints)]
        return np.min(midpoints), saddle_edges

    def cluster_neighbors(self):
        # density of saddle if two clusters share border, 0 if no border is shared (row/col indices are clusters)
        shares_cluster_border = np.zeros(shape=(self.t.n_leaves_, self.t.n_leaves_), dtype=np.float32)
        # Loop through clusters
        for ul in range(self.t.n_leaves_):
            ba = self.t.leaf_labels_ == ul
            dummy_c1, dummy_c2 = self.A[ba, :].nonzero()
            pts_c1 = np.arange(self.A.shape[0])[ba][dummy_c1]
            pts_c2 = dummy_c2
            edges = np.vstack([pts_c1, pts_c2]).T
            # Get neighboring
            neighbors = np.unique(self.t.leaf_labels_[edges])
            neighbors = neighbors[neighbors != ul]
            for neigh in neighbors:
                if (shares_cluster_border[ul, neigh] == 0) and (shares_cluster_border[neigh, ul] == 0):
                    # Distance to the knn'th nearest neighbor from the saddle point between both clusters
                    saddle_knndist, saddle_edges = self.dist_saddle_maxmean(
                        ba_cluster_base=ba,
                        ba_cluster_to_merge=self.t.leaf_labels_ == neigh
                    )
                    # Store least dense point (=max distance) of saddle -> important for merging condition
                    shares_cluster_border[ul, neigh] = max(saddle_knndist,
                                                           self.dists_to_knn[saddle_edges[0]],
                                                           self.dists_to_knn[saddle_edges[1]]
                                                           )
        self.cluster_borders = shares_cluster_border
        return

    def fit(self, alpha):
        data_idx = np.arange(self.data.shape[0])
        parents = np.arange(self.t.n_leaves_)
        cluster_modes = [data_idx[self.t.leaf_labels_ == i][
                             np.argmax(self.t.weights_[self.t.leaf_labels_ == i])]
                         for i in range(self.t.n_leaves_)
                         ]
        modes_density = [self.t.weights_[cluster_modes[i]] for i in range(self.t.n_leaves_)]

        self.cluster_neighbors()
        edges, columns = self.cluster_borders.nonzero()
        sorted_by_density = np.argsort(self.cluster_borders[edges, columns])
        # Loop through saddle points and merge clusters
        for e, c in zip(edges[sorted_by_density], columns[sorted_by_density]):
            e_parent = uf_find(e, parents)
            c_parent = uf_find(c, parents)
            # Cluster modes
            c1_mode = cluster_modes[e_parent]
            c2_mode = cluster_modes[c_parent]
            # Max distance of modes to knn'th neighbor
            d_max = max(self.dists_to_knn[c1_mode], self.dists_to_knn[c2_mode])
            d_saddle = self.cluster_borders[e, c]
            pval = self.compute_pvalue_simple(d_max=d_max, d_saddle=d_saddle)
            # If the pvalue is less then alpha we merge the peaks
            if (e_parent != c_parent) and (pval > alpha):
                uf_union(e_parent, c_parent, parents, modes_density)

        return np.array([uf_find(p, parents) for p in self.t.leaf_labels_], dtype=int)


