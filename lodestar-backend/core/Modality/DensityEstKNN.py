import numpy as np
from scipy.spatial import cKDTree


class DensityEstKNN:
    def __init__(self, X: np.ndarray = None, max_neighbors: int = None):
        """Class calculating densities on given data X
        max_neighbors: maximal neighbors to consider in knn density estimation
        """
        self.data = X
        self.max_neighbors = max_neighbors
        self.kd_tree = cKDTree(data=X)
        self.distances = self.calc_distances()

    def calc_distances(self):
        dists = None
        if (self.data is not None) and (self.max_neighbors is not None):
            dists, _ = self.kd_tree.query(self.data, k=self.max_neighbors+1, n_jobs=-1)
            dists = np.sort(dists[:, 1:], axis=1)
        return dists

    def build(self, X: np.ndarray = None, max_neighbors: int = None):
        self.data = X
        self.max_neighbors = max_neighbors
        self.distances = self.calc_distances()

    def knn_density(self, k_neighbors: int):
        if self.max_neighbors < k_neighbors:
            raise ValueError('Given k_neighbors is larger than max_neighbors')
        return 1 / np.sqrt(np.mean(np.square(self.distances[:, :k_neighbors]), axis=1))

    def save(self, fname):
        np.savez(fname, X=self.data, distances=self.distances, )

    def load(self, fname):
        npzfile = np.load(fname)
        self.data = npzfile['X']
        self.distances = npzfile['distances']
        self.max_neighbors = self.distances.shape[1]
