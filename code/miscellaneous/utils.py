import numpy as np


# Flatten a list of lists
def flatten_listlist(list_list):
    return [item for sublist in list_list for item in sublist]


def pairwise_loop(iterable):
    return zip(iterable, iterable[1:])


def constrain_range(arr, lo=0, hi=1):
    return arr[(arr >= lo) & (arr <= hi)]


def isin_constrained_range(arr, lo=0, hi=1):
    return (arr >= lo) & (arr <= hi)
