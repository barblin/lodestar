import numpy as np
from sklearn.mixture import GaussianMixture


def gmm_cut(data2fit, n_components=2):
    """Fit a gaussian mixture to the given 1D data and output classification parameters"""
    max_value_per_class = []
    n_trials = 0
    while len(max_value_per_class) != n_components:  # Sometimes a GMM will only output 1 component -> check for that
        # Train the GMM on the input data
        gmm = GaussianMixture(n_components=n_components).fit(data2fit.reshape(-1, 1))
        gmm_lbls = gmm.predict(data2fit.reshape(-1, 1))   # implement also probability estimate predict_proba(X)
        # Get maximum value per class
        max_value_per_class = [np.max(data2fit[gmm_lbls == li]) for li in np.unique(gmm_lbls)]
        # Fail save
        if n_trials > 50:
            print(f'Input unable to be clustered into {n_components} classes')
            return None, None, None, False
        n_trials += 1

    # -> Sort in descending order by maximum density, then take the second highest one
    low_density_cluster = np.argsort(max_value_per_class)[::-1][1]
    # Maximium value of 2nd highest value/denisty cluster
    th = np.max(data2fit[gmm_lbls == low_density_cluster])
    # Maximum value/density class is the one with larger values than the maximum of the 2nd highest class values
    cluster_labels = data2fit > th
    return gmm, cluster_labels, th, True
