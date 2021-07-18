import numpy as np
from sklearn.neighbors import KernelDensity, NearestNeighbors
import pandas as pd
from LineGeometry.sample_path_linear import sample_along_path
from LineGeometry.utils import track_length
from LineGeometry.line_projection import projected_distances_on_line
from Modality.modality_base import ModalityBase
from scipy.interpolate import InterpolatedUnivariateSpline as ipu_spline
import diptest


class KdeModality(ModalityBase):
    """Test modality conditions (single-/multi modal) between modes found in the data using
    a KDE estimate of the density
    """
    def __init__(self, data, max_dist, nb_neighbors):
        super().__init__(data=data, max_dist=max_dist, nb_neighbors=nb_neighbors, suppress_kde=False)

    def density_track_kde_full(self, interpolated_track):
        density_along_track = np.exp(self.kde_obj.score_samples(interpolated_track))
        # Renormalize data with integral (estimated via trapezian rule)
        renormed_data = density_along_track / np.trapz(density_along_track.ravel(),
                                                       np.linspace(0, track_length(interpolated_track),
                                                                   density_along_track.size).ravel())
        # Compute eCDF
        cdf = np.cumsum(renormed_data)
        cdf = cdf / cdf[-1]
        return renormed_data, cdf

    def test_multimodality(self, sh_path, alpha, random=False):
        """Approximate dip test via KDE density estimate"""
        # Projected samples within max_dist -> corresponds to the number of samples drawn from eCDF
        data_proj = projected_distances_on_line(line_anchors=self.data.iloc[sh_path].values, data=self.data.values,
                                                max_dist=self.max_dist)
        # KDE samples
        interpol = sample_along_path(line_anchors=self.data.iloc[sh_path].values, step_size=0.1 * self.max_dist,
                                     dist_extrapoate=self.max_dist)
        _, ecdf = self.density_track_kde_full(interpol)
        # Create spline mapping f-1(x) = y
        f_inv = ipu_spline(ecdf, np.linspace(0, track_length(interpol), ecdf.size))

        if random:
            # Random sampling: currently hard coded to 25 runs
            data_samples = f_inv(np.random.uniform(0, 1, size=data_proj.shape[0]))
            ndips = [diptest.diptest(f_inv(np.random.uniform(0, 1, size=data_proj.shape[0])))[1] for _ in range(25)]
            dk = np.median(ndips)
        else:
            # Suppress randomness and keep CDF as from KDE
            data_samples = f_inv(np.linspace(0, 1, data_proj.shape[0]))
            dk = diptest.diptest(data_samples)[1]

        return dk > alpha, data_samples
