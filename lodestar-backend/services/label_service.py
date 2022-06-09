from config.config import COL_LABEL, alpha_values
from services.data.session_source import get_session


def get_labels_all(data):
    level = data["level"]

    labels = {}

    for alpha in alpha_values:
        labels[alpha] = get_labels(level, alpha, data)

    return labels


def get_labels(level, alpha, data):
    current_cluster = None

    if "current_cluster" in data.keys():
        current_cluster = data["current_cluster"]

    if level is not None and alpha is not None:
        x = get_session(level, alpha)
        x = x[COL_LABEL]
        x.dropna()

        if current_cluster is not None:
            index = x.index
            cluster_indices = index[x != float(current_cluster)]
            x.loc[cluster_indices.tolist()] = -1.0

        return x.astype(int).values.tolist()

    return []
