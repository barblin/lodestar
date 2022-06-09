from services.data.datasource import data_dict
from services.data.df_service import csv2pandas


def get(filename):
    features, _ = csv2pandas(data_dict()[filename])
    max_x = 0
    max_y = 0
    clusters = {}
    for i in range(0, len(features.f1.keys())):
        x = float(features.f1[i])
        y = float(features.f2[i])

        if max_x < x:
            max_x = x

        if max_y < y:
            max_y = y

        label = int(features.labels[i])

        if label not in clusters.keys():
            clusters[label] = []

        clusters[label].append([x, y, label])

    features = {'clusters': clusters, 'max_x': max_x, 'max_y': max_y}

    return features
