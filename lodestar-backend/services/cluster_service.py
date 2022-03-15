from config.config import COL_LABEL
from services.data.session_source import get_session, get_session_name, \
  store_for_level


def update_cluster(lid, cid, data):
  custom_label = data["custom_label"]
  custom_label_name = data["custom_label_name"]

  print(custom_label_name)

  x = get_session(lid)

  index = x.index
  cluster_index = index[x[COL_LABEL] == float(cid)]
  x.loc[cluster_index.tolist(), 'custom_label'] = custom_label
  x.loc[cluster_index.tolist(), 'custom_label_name'] = custom_label_name

  store_for_level(x, get_session_name(lid))

  x = x[COL_LABEL]
  return x.astype(str).values.tolist()
