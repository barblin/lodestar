import pandas as pd

from config.config import p_scaling, v_scaling


def prepare_columns(data_axes):
    columns = [data_axes["s1"], data_axes["s2"], data_axes["s3"],
               data_axes["v1"], data_axes["v2"]]
    plot_radial = data_axes["v3"] is not None

    if plot_radial:
        columns.append(data_axes["v3"])

    return columns


def select_dataframe(data, columns):
    df_cluster = data
    df_cluster = df_cluster[columns]
    df_cluster.dropna()

    return scale_dataframe_features(df_cluster, columns)


def scale_dataframe_features(df_cluster, columns):
    df_cluster[columns[3:]] *= v_scaling
    df_cluster[columns[:3]] *= p_scaling

    return df_cluster


def csv2pandas(data_info):
    x = pd.read_csv(data_info['path'], **data_info['read_csv_kwargs'])
    x = x[data_info['columns2keep']]
    x = x.rename(columns=data_info['rename_columns'])
    x = x.dropna()
    x = x.astype(data_info['astype'])
    return x, data_info['columns2keep']


def get_columns_from_dataframe_cluster(data_info):
    return pd.read_csv(data_info['path'])


def get_dataframe_cluster(data_info):
    x, _ = csv2pandas(data_info)
    cluster_cols = ['f1', 'f2']
    return x, x[cluster_cols]


def get_dataframe_headers(data_info):
    return pd.read_csv(data_info['path']).columns
