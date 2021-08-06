from services.data.datasource import data_dict


def list_content():
    return list(data_dict().keys())
