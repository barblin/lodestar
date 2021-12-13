import os

from config.config import export_location
from services.data.level_source import file_suffix

export_post = "_labeled"


def get_export_path(df, filename):
    export_file_name = filename + export_post + file_suffix
    return store_export(df, export_file_name)


def store_export(df, filename):
    if not os.path.exists(export_location()):
        os.mkdir(export_location())

    return __write_overwrite(df, filename)


def __write_overwrite(df, filename):
    file = export_location() + filename
    df.to_csv(file)
    return file
