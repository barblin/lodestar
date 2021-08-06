import pandas as pd


def csv2pandas(data_info):
    x = pd.read_csv(data_info['path'], **data_info['read_csv_kwargs'])
    x = x[data_info['columns2keep']]
    x = x.rename(columns=data_info['rename_columns'])
    x = x.dropna()
    x = x.astype(data_info['astype'])
    return x, data_info['columns2keep']


def get_dataframe_cluster(data_info):
    x, _ = csv2pandas(data_info)
    cluster_cols = ['f1', 'f2']
    return x, x[cluster_cols]
