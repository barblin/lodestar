from services.data.datasource import data_dict
from services.df_service import csv2pandas


def get(filename):
    features, _ = csv2pandas(data_dict()[filename])

    data = []
    max_x = 0
    max_y = 0
    for i in range(0, len(features.f1.keys())):
        x = float(features.f1[i])
        y = float(features.f2[i])

        if max_x < x:
            max_x = x

        if max_y < y:
            max_y = y

        data.append([x, y, int(features.labels[i])])

    features = {'data': data, 'max_x': max_x, 'max_y': max_y}

    return features
