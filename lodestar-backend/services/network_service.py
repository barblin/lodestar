import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from api.network_response import NetworkResponse
from services.data.datasource import data_dict
from services.data.df_service import prepare_columns, select_dataframe, \
    get_columns_from_dataframe_cluster
from services.density_service import scale_space_dense_components
from services.graph.tomato_ext_service import create_graph


def get_cached_level(level):
    return NetworkResponse()


def get_join_tree(filename, data_axes):
    level = data_axes["level"]

    if level is not None:
        return recalculate_levels(filename, data_axes)

    return recalculate_levels(filename, data_axes)


def recalculate_levels(filename, data_axes):
    columns = prepare_columns(data_axes)
    data = get_columns_from_dataframe_cluster(data_dict()[filename])
    df_cluster = select_dataframe(data, columns)
    res, te = create_graph(df_cluster)
    sst = scale_space_dense_components(data, te, columns, df_cluster)

    ssp_clusters = sst.scale_space_clusters
    g_ssp = nx.Graph()
    g_ssp.add_nodes_from(ssp_clusters.keys())

    node_level_clusters = {}
    for cli in ssp_clusters.keys():
        node_level_clusters[cli] = [int(ssp_clusters[cli].level_id),
                                    int(ssp_clusters[cli].nb_points),
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
