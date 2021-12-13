from services.data.datasource import data_dict
from services.data.df_service import get_columns_from_dataframe_cluster
from services.util.util import clean_num


def get_space(filename, data):
    columns = [data["s1"], data["s2"], data["s3"]]
    solution = []

    x = get_columns_from_dataframe_cluster(data_dict()[filename])
    x = x[columns]
    x.dropna()
    for j in x.iterrows():
        solution.append({'x': clean_num(j[1][0]), 'y': clean_num(j[1][1]),
                         'z': clean_num(j[1][2])})

    return solution
