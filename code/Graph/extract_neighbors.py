import numpy as np
from miscellaneous.utils import flatten_listlist


def neighboring_modes(cluster_modes, G, nb_neighbors=1):
    """Get neighoring modes in MST graph with saddle points and modes
        nb_neighbors: number of neighboring shells to serach for neighboring peaks
    """
    full_list = []
    curr_cluster_modes = cluster_modes
    for _ in range(nb_neighbors):
        # direct neighbors of a peak are saddle points
        nbs_saddle = [list(int(n) for n in G.neighbors(cmd)) for cmd in curr_cluster_modes]
        # neighbors of these saddle pts are the neighboring peaks
        nbs_modes = []
        for i, nn in enumerate(nbs_saddle):
            nbs_modes.append(
                flatten_listlist([list(int(n) for n in G.neighbors(saddle) if n not in full_list) for saddle in nn]))

        all_nbs = flatten_listlist(nbs_modes)
        full_list.extend(all_nbs)
        curr_cluster_modes = all_nbs
    return np.union1d(full_list, cluster_modes)