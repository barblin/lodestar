from services.data.datasource import data_dict
from services.data.df_service import get_columns_from_dataframe_cluster
from services.util.util import clean_num


def get_velocity(filename, data):
    columns = [data["v1"], data["v2"]]
    plot_radial = data["v3"] is not None

    solution = []

    if plot_radial:
        columns.append(data["v3"])

    x = get_columns_from_dataframe_cluster(data_dict()[filename])
    x = x[columns]

    for row in x.iterrows():
        solution.append(create_entry(row))

    return solution


def create_entry(row):
    return {'x': clean_num(row[1][0]), 'y': clean_num(row[1][1]),
            'z': clean_num(row[1][2])}


def get_radial(filename, data):
    solution = []
    columns = [data["v3"]]

    x = get_columns_from_dataframe_cluster(data_dict()[filename])
    x = x[columns]
    x.dropna()

    for row in x.iterrows():
        solution.append(clean_num(row[1][0]))

    return solution
