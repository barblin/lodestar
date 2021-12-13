import os

import pandas as pd

from config.config import session_location, COL_LABEL, \
    COL_CUSTOM_LABEL, COL_CUSTOM_LABEL_NAME
from services.data.level_source import file_suffix, level_pre, get_level

session_pre = "session_"


def store_for_level(df, filename):
    if not os.path.exists(session_location()):
        os.mkdir(session_location())

    __write_overwrite(df, filename)


def get_session(level):
    session_file_name = session_pre + level_pre + str(level) + file_suffix

    if os.path.isfile(session_file_name):
        return pd.read_csv(session_file_name)
    else:
        df = get_level(level)
        df[COL_CUSTOM_LABEL] = df[COL_LABEL]
        df[COL_CUSTOM_LABEL_NAME] = df[COL_LABEL]
        filtered = df[[COL_LABEL, COL_CUSTOM_LABEL, COL_CUSTOM_LABEL_NAME]]
        store_for_level(filtered, session_file_name)
        return filtered


def __write_overwrite(df, filename):
    file = session_location() + filename
    df.to_csv(file)
