from os import walk

from config.config import import_location


def data_dict():
    f = []
    for (dirpath, dirnames, filenames) in walk(import_location()):
        f.extend(filenames)

    resources = {}
    for filename in f:
        name = filename.split('.')[0]
        resources[name] = {'path': import_location() + filename}

    return resources
