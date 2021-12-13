import os

import pandas as pd

from config.config import level_location

edge_sep = ";"
vex_sep = ","
level_pre = "level_"
file_suffix = ".csv"


def store_for_level(df, filename):
    if not os.path.exists(level_location()):
        os.mkdir(level_location())

    __write_overwrite(df, level_pre + filename + file_suffix)


def get_level(level):
    return __read(level_pre + str(level) + file_suffix)


def __string_to_coords(coords_string):
    return [float(x) for x in coords_string.split(vex_sep)]


def __write_overwrite(df, filename):
    file = level_location() + filename
    df.to_csv(file)


def __read(filename):
    try:
        file = level_location() + filename
        return pd.read_csv(file)
    except FileNotFoundError:
        return ""
