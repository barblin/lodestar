from services.data import df_service
from services.data.datasource import data_dict


def list_content():
    return list(data_dict().keys())


def get_resource_headers(filename):
    return list(df_service.get_dataframe_headers(
        data_dict()[filename]))
