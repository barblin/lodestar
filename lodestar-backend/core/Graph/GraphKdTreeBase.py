import numpy as np
import nglpy
from scipy.stats import norm
from scipy.sparse import csr_matrix
from scipy.spatial import cKDTree


def compute_pvalue(k, p, d_max, d_saddle):
    SB_alpha = p * np.sqrt(k / 2) * (np.log(d_saddle) - np.log(d_max))
    return 1 - norm.cdf(SB_alpha)


class GraphPreparation:
    def __init__(self, data, max_neighbors, beta):
        self.data = data
        self.max_neighbors = max_neighbors
        self.beta = beta
        self.A = self.beta_adjacency(data, max_neighbors=max_neighbors, beta=beta)

    @staticmethod
    def beta_adjacency(X, max_neighbors, beta):
        # Build beta skeleton
        erg = nglpy.EmptyRegionGraph(max_neighbors=max_neighbors, relaxed=False, beta=beta)
        erg.build(X)
        rows, cols = [], []
        for i, (node, edges) in enumerate(erg.neighbors().items()):
            rows.extend(len(edges) * [node])
            cols.extend(list(edges))
        return csr_matrix((np.ones_like(rows), (rows, cols)), shape=(X.shape[0], X.shape[0]))


class ClusterPreparation(GraphPreparation):
    def __init__(self, data, max_neighbors, beta, knn):
        """
        :param max_neighbors: maximal number of neighbors considered as graph edges
        :param beta: structure parameter of beta skeleton
        :param knn: Number of neighbors for
        """
        super().__init__(data=data, max_neighbors=max_neighbors, beta=beta)
        self.knn = knn
        self.kd_tree = cKDTree(data=data)
        self.dists_to_knn = self.kneighbors(k_neighbors=knn)
        # Remove edges with significant dip:
        self.A = self.remove_edges()
        # Set midpoints of beta graph
        self.set_midpoints()

    def kneighbors(self, k_neighbors):
        dists, _ = self.kd_tree.query(self.data, k=k_neighbors, n_jobs=-1)
        dists = np.max(dists, axis=1)
        return dists

    def update_kdtree(self, knn):
        self.knn = knn
        self.dists_to_knn = self.kneighbors(k_neighbors=knn)
        self.set_midpoints()

    def remove_edges(self):
        # We remove edges where the mid-points between 2 vertices has a significant dip
        # --> we choose 7 neighbors for this test to be aware of local changes
        knn_test = 7
        e1, e2 = self.A.nonzero()
        # midpts = (self.data.iloc[e1].values + self.data.iloc[e2].values) * 0.5   <-- previous version with dataframes
        midpts = (self.data[e1] + self.data[e2]) * 0.5
        dists_midpoints, _ = self.kd_tree.query(midpts, k=knn_test, n_jobs=-1)
        d_saddle = np.max(dists_midpoints, axis=1)
        dists = self.kneighbors(knn_test)
        d_max = np.max(np.vstack([dists[e1], dists[e2]]), axis=0)
        pvals = compute_pvalue(k=knn_test, p=self.data.shape[-1], d_max=d_max, d_saddle=d_saddle)
        keep_edges = pvals > 0.05  # 5% significance level
        rows, cols = e1[keep_edges], e2[keep_edges]
        A = csr_matrix((np.ones_like(rows), (rows, cols)), shape=(self.data.shape[0], self.data.shape[0]))
        return A

    def set_midpoints(self):
        # Extract all midpoints
        e1, e2 = self.A.nonzero()
        # m = (self.data.iloc[e1].values + self.data.iloc[e2].values) * 0.5   <-- previous version with dataframes
        m = (self.data[e1] + self.data[e2]) * 0.5
        # Get distances to knn'th neighbor of midpoints in beta graph
        dists_from_midpoints, _ = self.kd_tree.query(m, k=self.knn, n_jobs=-1)
        dists_from_midpoints = np.max(dists_from_midpoints, axis=1)
        # Store knn distances of midpoints in adjacency matrix
        self.A.data = dists_from_midpoints

    @staticmethod
    def get_n_midpoints(p1, p2, n_midpoints, flattened=False):
        x_vals = np.linspace(0, 1, n_midpoints + 1)[1:-1]
        midpoints = p1 + (p2 - p1) * x_vals.reshape(x_vals.size, 1, 1)
        midpoints = midpoints.T.reshape((p1.shape[-1], x_vals.size * p1.shape[0])).T
        if flattened:
            return midpoints
        else:
            return midpoints.reshape((p1.shape[0], n_midpoints - 1, p1.shape[-1]))



