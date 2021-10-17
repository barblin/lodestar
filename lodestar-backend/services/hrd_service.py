from services.data.datasource import data_dict
from services.data.df_service import get_columns_from_dataframe_cluster
from services.util.util import clean_num


def get_hrd(filename, data):
  columns = [data["x"], data["y"]]

  x = get_columns_from_dataframe_cluster(data_dict()[filename], columns)
  x = x[columns]
  x.dropna()

  solution = []
  for j in x.iterrows():
    solution.append({'x': clean_num(j[1][0]), 'y': clean_num(j[1][1])})

  return solution
