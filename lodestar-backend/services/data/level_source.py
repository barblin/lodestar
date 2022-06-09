from pathlib import Path

import pandas as pd

from config.config import level_location

edge_sep = ";"
vex_sep = ","
level_pre = "level_"
file_suffix = ".csv"


def store_for_level(df, filename, alpha):
    Path(level_location(alpha)).mkdir(parents=True, exist_ok=True)

    __write_overwrite(df, level_pre + filename + file_suffix, alpha)


def get_level(level, alpha):
    return __read(level_pre + str(level) + file_suffix, alpha)


def __string_to_coords(coords_string):
    return [float(x) for x in coords_string.split(vex_sep)]


def __write_overwrite(df, filename, alpha):
    file = level_location(alpha) + filename
    df.to_csv(file)


def __read(filename, alpha):
    try:
        file = level_location(alpha) + filename
        return pd.read_csv(file)
    except FileNotFoundError:
        return ""
