from services.data.datasource import data_dict
from services.data.df_service import get_columns_from_dataframe_cluster
from services.util.util import clean_num


def get_velocity(filename, data):
  columns = [data["v1"], data["v2"]]
  plot_radial = data["v3"] is not None

  if plot_radial:
    columns.append(data["v3"])

  x = get_columns_from_dataframe_cluster(data_dict()[filename], columns)
  x = x[columns]

  solution = []
  for row in x.iterrows():
    solution.append(create_entry(row, plot_radial))

  return solution


def create_entry(row, plot_radial):
  if plot_radial:
    return {'x': clean_num(row[1][0]), 'y': clean_num(row[1][1]),
            'z': clean_num(row[1][2])}

  return {'x': clean_num(row[1][0]), 'y': clean_num(row[1][1])}
