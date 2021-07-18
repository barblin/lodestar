import numpy as np
from sklearn.mixture import GaussianMixture


def gmm_cut(data2fit, n_components=2):
    """Fit a gaussian mixture to the given 1D data and output classification parameters"""
    # Train the GMM on the input data
    gmm = GaussianMixture(n_components=n_components).fit(data2fit.reshape(-1, 1))
    gmm_lbls = gmm.predict(data2fit.reshape(-1, 1))   # implement also probability estimate predict_proba(X)
    # it might happen that the right cluster gets very low density points as well as the cluster might be very flat
    # -> remove with min-density clause
    # -> Sort in descending order by maximum density, then take the second highest one
    low_density_cluster = np.argsort([np.max(data2fit[gmm_lbls == li])
                                      for li in np.unique(gmm_lbls)])[::-1][1]
    th = np.max(data2fit[gmm_lbls == low_density_cluster])
    cluster_labels = data2fit > th
    return gmm, cluster_labels, th
