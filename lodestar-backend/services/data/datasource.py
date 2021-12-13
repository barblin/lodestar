import numpy as np


def data_dict():
    return {
      'GaiaSource-1000172165251650944-1000424567594791808': {
        'path': './resources/GaiaSource-1000172165251650944'
                '-1000424567594791808.csv',
        'read_csv_kwargs': {},
        'columns2keep': ['V2', 'V3', 'V4'],
        'rename_columns': {'V2': 'f1', 'V3': 'f2', 'V4': 'labels'},
        'astype': {'f1': np.float32, 'f2': np.float32, 'labels': np.int32},
      },
      'GaiaSource_000-020-090': {
        'path': './resources/GaiaSource_000-020-090.csv',
        'read_csv_kwargs': {},
        'columns2keep': ['V2', 'V3', 'V4'],
        'rename_columns': {'V2': 'f1', 'V3': 'f2', 'V4': 'labels'},
        'astype': {'f1': np.float32, 'f2': np.float32, 'labels': np.int32},
      },
      'skinnyDipData_8': {
        'path': './resources/skinnyDipData_8.csv',
        'read_csv_kwargs': {},
        'columns2keep': ['V2', 'V3', 'V4'],
        'rename_columns': {'V2': 'f1', 'V3': 'f2', 'V4': 'labels'},
        'astype': {'f1': np.float32, 'f2': np.float32, 'labels': np.int32},
      },
      'waveData_8': {
        'path': './resources/waveData_8.csv',
        'read_csv_kwargs': dict(header=None, names=['f1', 'f2', 'labels']),
        'columns2keep': ['f1', 'f2', 'labels'],
        'rename_columns': {},
        'astype': {'f1': np.float32, 'f2': np.float32, 'labels': np.int32}
      },
      'cluster_data_uppersco_extravel_covmtx': {
        'path': './resources/cluster_data_uppersco_extravel_covmtx.csv',
        'read_csv_kwargs': dict(header=None, names=['f1', 'f2', 'labels']),
        'columns2keep': ['f1', 'f2', 'labels'],
        'rename_columns': {},
        'astype': {'f1': np.float32, 'f2': np.float32, 'labels': np.int32}
      }
    }
