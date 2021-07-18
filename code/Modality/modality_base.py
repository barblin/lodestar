import numpy as np
from sklearn.neighbors import KernelDensity, NearestNeighbors


class ModalityBase:
    """Base class for modality calculations"""
    def __init__(self, data, max_dist=None, nb_neighbors=None, suppress_kde=False):
        self.data = data
        self.max_dist = max_dist
        self.nb_neighbors = nb_neighbors
        self.nn = NearestNeighbors(algorithm='ball_tree', n_jobs=-1).fit(data)
        self.suppress_kde = suppress_kde
        self.kde_obj = None
        # ---- Compute member vars -----
        self.update(max_dist, nb_neighbors)

    def update(self, max_dist=None, nb_neighbors=None):
        # 1) max dist if none
        # Calculate max dist from the average distance to the
        if max_dist is None:
            if nb_neighbors is not None:
                dist, _ = self.nn.kneighbors(n_neighbors=self.nb_neighbors, return_distance=True)
                # don't take the mean maximum distance to the k nearest neighbors to remove outliers
                self.max_dist = np.median(np.percentile(dist, q=90, axis=1))
            else:
                raise ValueError('At least max_dist or nb_neighbors has to be set')

        # 2) KDE
        if not self.suppress_kde:
            self.update_kde(self.max_dist/2)

    def update_kde(self, new_max_dist):
        # Kwargs hardcoded thus far
        kde_kwargs = dict(algorithm='auto', kernel='gaussian', metric='euclidean', atol=1e-7, rtol=1e-6)
        self.kde_obj = KernelDensity(bandwidth=new_max_dist, **kde_kwargs).fit(self.data)
