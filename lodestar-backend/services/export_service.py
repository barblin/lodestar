from services.data.datasource import data_dict
from services.data.df_service import get_columns_from_dataframe_cluster
from services.data.export_source import get_export_path
from services.data.session_source import get_session


def export_file(filename, level, alpha):
  x = get_columns_from_dataframe_cluster(data_dict()[filename])
  session = get_session(level, alpha)
  export = x.join(session)

  return get_export_path(export, filename)
