import numpy as np
from code.LineGeometry.line_projection import projected_distances_on_line
from code.LineGeometry.sample_path_linear import sample_along_path
from code.LineGeometry.utils import track_length
import diptest
from scipy.stats import norm


def density_track_distance(nn, interpolated_track, n_neighbors=30):
    """Compute distance to n'th nearest neighbor"""
    dist, _ = nn.kneighbors(X=interpolated_track, n_neighbors=n_neighbors, return_distance=True)
    return dist[:,-1]


def is_multimodal_knn(X, nn, interpolated_track, n_neighbors, alpha=0.01):
    """
    Multidimensional test for multimodality, from
    Burman & Polonik 2009: Multivariate mode hunting: Data analytic
    tools with measures of significance. Journal of Multivariate
    Analysis 100 (2009).
    """
    p = X.shape[-1]
    d_knn = density_track_distance(nn, interpolated_track=np.vstack(interpolated_track).T, n_neighbors=n_neighbors)
    SB_alpha = p*(np.log(d_knn) - np.log(max(d_knn[0], d_knn[-1])))
    return (not (SB_alpha >= np.sqrt(2./n_neighbors)*norm.ppf(1-alpha)).any()), SB_alpha, np.sqrt(2./n_neighbors)*norm.ppf(1-alpha)


class DataModality:
    """Test modality conditions (single-/multi modal) between modes found in the data by studying the projection
    of data onto a line
    """
    def __init__(self, data):
        self.data = data

    def test_multimodality(self, sh_path, max_dist, knn_nn, knn_nb_neighbs, alpha=0.01, min_nb_project=100):
        # 1) Projection test
        data_proj = projected_distances_on_line(line_anchors=self.data.iloc[sh_path].values, data=self.data.values,
                                                max_dist=max_dist)  # max_dist)
        # If the minimum number of points are to small use knn test
        if len(data_proj) < min_nb_project:
            len_track = track_length(self.data.iloc[sh_path].values)
            nb_samples = 200   # hard-coded for now
            interpol = sample_along_path(line_anchors=self.data.iloc[sh_path].values, step_size=len_track/nb_samples,
                                         dist_extrapoate=None)
            # KNN multimodality estiamation
            significant_multimodal, _, _ = is_multimodal_knn(X=self.data, nn=knn_nn, interpolated_track=interpol,
                                                             n_neighbors=min(knn_nb_neighbs, len(data_proj) // 2),
                                                             alpha=alpha)
            return significant_multimodal

        # If enough projected members
        _, pval_projected = diptest.diptest(data_proj)
        significant_multimodal = pval_projected > alpha
        return significant_multimodal
