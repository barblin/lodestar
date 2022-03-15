import os

import pandas as pd

from config.config import session_location, COL_LABEL, \
    COL_CUSTOM_LABEL, COL_CUSTOM_LABEL_NAME
from services.data.level_source import file_suffix, level_pre, get_level

session_pre = "session_"


def store_for_level(df, filename, alpha):
    if not os.path.exists(session_location(alpha)):
        os.mkdir(session_location(alpha))

    __write_overwrite(df, filename, alpha)


def get_session_name(level):
    return session_pre + level_pre + str(level) + file_suffix


def get_session(level, alpha):
    session_file_name = get_session_name(level)

    if os.path.isfile(session_location(alpha) + session_file_name):
        return pd.read_csv(session_location(alpha) + session_file_name)
    else:
        df = get_level(level, alpha)
        df[COL_CUSTOM_LABEL] = df[COL_LABEL]
        df[COL_CUSTOM_LABEL_NAME] = df[COL_LABEL]
        filtered = df[[COL_LABEL, COL_CUSTOM_LABEL, COL_CUSTOM_LABEL_NAME]]
        store_for_level(filtered, session_file_name, alpha)
        return filtered


def __write_overwrite(df, filename, alpha):
    file = session_location(alpha) + filename
    df.to_csv(file)
