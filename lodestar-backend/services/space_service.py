import math

from services.data.datasource import data_dict
from services.df_service import get_columns_from_dataframe_cluster


def get_space(filename, data):
  columns = [data["s1"], data["s2"], data["s3"]]
  x = get_columns_from_dataframe_cluster(data_dict()[filename], columns)
  x = x[columns]
  x.dropna()

  solution = []
  for j in x.iterrows():
    solution.append({'x': clean_num(j[1][0]), 'y': clean_num(j[1][1]),
                     'z': clean_num(j[1][2])})

  return solution


def clean_num(num):
  conv = float(num)

  if math.isnan(conv):
    return float(0)

  return conv
