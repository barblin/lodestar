import json

import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from api.network_response import NetworkResponse
from config.config import get_alpha_array, alpha_values
from services.data.datasource import data_dict
from services.data.df_service import prepare_columns, select_dataframe, \
    get_columns_from_dataframe_cluster
from services.data.tree_source import store_for_alpha, get_tree
from services.density_service import scale_space_dense_components
from services.significant_roots_service import collect_roots


def get_current_tree(data):
    alpha = data["alpha"]
    return get_tree(str(alpha))


def get_trees():
    trees = {}

    for alpha in alpha_values:
        tree = json.loads(get_tree(str(alpha)))
        trees[alpha] = tree["node_level_clusters"]

    return trees


def get_significant_roots(data):
    level = int(data["level"])
    unique_roots = set(())
    alpha_nodes = {}

    for alpha in alpha_values:
        tree = json.loads(get_tree(str(alpha)))
        roots = collect_roots(tree["node_level_clusters"], level)
        unique_roots.update(roots)
        alpha_nodes[alpha] = roots

    return {"unique_nodes": list(unique_roots), "alpha_nodes": alpha_nodes}


def produce_join_trees(filename, data_axes):
    for alpha in get_alpha_array():
        response = recalculate_levels(filename, data_axes, alpha)
        json = response.jsonify()
        store_for_alpha(json, alpha)


def recalculate_levels(filename, data_axes, alpha):
    columns = prepare_columns(data_axes)
    data = get_columns_from_dataframe_cluster(data_dict()[filename])
    df_cluster = select_dataframe(data, columns[:5])
    sst = scale_space_dense_components(data, columns, df_cluster, alpha)

    ssp_clusters = sst.scale_space_clusters
    g_ssp = nx.Graph()
    g_ssp.add_nodes_from(ssp_clusters.keys())

    node_level_clusters = {}
    for cli in ssp_clusters.keys():
        node_level_clusters[cli] = [int(ssp_clusters[cli].level_id),
                                    int(len(ssp_clusters[cli].index_arr)),
                                    int(ssp_clusters[cli].mode)]
        for child in ssp_clusters[cli].child_list:
            g_ssp.add_edge(cli, child)

    pos = graphviz_layout(g_ssp, prog="dot")

    max_x = 0
    max_y = 0
    for key in pos:
        pos[key] = list(pos[key])

        if max_x < pos[key][0]:
            max_x = pos[key][0]
        if max_y < pos[key][1]:
            max_y = pos[key][1]

    edges = dict(g_ssp.edges.keys())
    nodes = list(g_ssp.nodes)

    return NetworkResponse(dict(pos), nodes, node_level_clusters,
                           edges, max_x, max_y)
