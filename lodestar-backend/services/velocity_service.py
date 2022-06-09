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

  minx = 10000000
  maxx = 0
  miny = 10000000
  maxy = 0

  for row in x.iterrows():
    cur_x = clean_num(row[1][0])
    cur_y = clean_num(row[1][1])
    cur_z = clean_num(row[1][2])

    if cur_x < minx:
      minx = cur_x

    if maxx < cur_x:
      maxx = cur_x

    if cur_y < miny:
      miny = cur_y

    if maxy < cur_y:
      maxy = cur_y

    solution.append({'x': cur_x, 'y': cur_y, 'z': cur_z})

  return {"solution": solution, "minx": minx, "maxx": maxx, "miny": miny,
          "maxy": maxy}
