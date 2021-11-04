import numpy as np
import nglpy
from scipy.sparse import csr_matrix
from scipy.spatial import cKDTree


class GraphPreparation:
    def __init__(self, data, max_neighbors, beta):
        self.data = data
        self.max_neighbors = max_neighbors
        self.beta = beta
        self.A = self.beta_adjacency()

    def beta_adjacency(self):
        # Build beta skeleton
        erg = nglpy.EmptyRegionGraph(max_neighbors=self.max_neighbors, relaxed=False, beta=self.beta)
        erg.build(self.data.values)
        rows, cols = [], []
        for i, (node, edges) in enumerate(erg.neighbors().items()):
            rows.extend(len(edges) * [node])
            cols.extend(list(edges))
        return csr_matrix((np.ones_like(rows), (rows, cols)), shape=(self.data.shape[0], self.data.shape[0]))


class ClusterPreparation(GraphPreparation):
    def __init__(self, data, max_neighbors, beta, knn):
        super().__init__(data=data, max_neighbors=max_neighbors, beta=beta)
        self.knn = knn
        self.kd_tree = cKDTree(data=data.values)
        self.dists_to_knn = self.kneighbors(k_neighbors=knn)
        # Set midpoints of beta graph
        self.set_midpoints()

    def kneighbors(self, k_neighbors):
        dists, _ = self.kd_tree.query(self.data.values, k=k_neighbors, n_jobs=-1)
        dists = np.max(dists, axis=1)
        return dists

    def update_kdtree(self, knn):
        self.knn = knn
        self.dists_to_knn = self.kneighbors(k_neighbors=knn)
        self.set_midpoints()

    def set_midpoints(self):
        # Extract all midpoints
        e1, e2 = self.A.nonzero()
        m = (self.data.iloc[e1].values + self.data.iloc[e2].values) * 0.5
        # Get distances to knn'th neighbor of midpoints in beta graph
        dists_from_midpoints, _ = self.kd_tree.query(m, k=self.knn, n_jobs=-1)
        dists_from_midpoints = np.max(dists_from_midpoints, axis=1)
        # Store knn distances of midpoints in adjacency matrix
        self.A.data = dists_from_midpoints


