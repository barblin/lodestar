import json
from pathlib import Path

from config.config import alpha_location, get_alpha_array
import shutil

alpha_pre = "alpha_"


def clear_cache():
    for alpha in get_alpha_array():
        shutil.rmtree(alpha_location(alpha))


def store_for_alpha(tree, alpha):
    Path(alpha_location(alpha)).mkdir(parents=True, exist_ok=True)
    __write_overwrite(tree, alpha)


def __write_overwrite(tree, alpha):
    file = alpha_location(alpha) + "/tree.json"

    with open(file, 'w') as outfile:
        json.dump(tree, outfile)


def get_tree(alpha):
    file = alpha_location(alpha) + "/tree.json"

    with open(file) as json_file:
        return json.load(json_file)
