import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from api.network_response import NetworkResponse
from services.data.datasource import data_dict
from services.density_service import scale_space_dense_components
from services.data.df_service import get_dataframe_cluster


def get_join_tree(filename):
    x, df_cluster = get_dataframe_cluster(data_dict()[filename])
    sst = scale_space_dense_components(x, df_cluster)

    ssp_clusters = sst.scale_space_clusters

    G_ssp = nx.Graph()
    G_ssp.add_nodes_from(ssp_clusters.keys())
    for cli in ssp_clusters.keys():
        for child in ssp_clusters[cli].child_list:
            G_ssp.add_edge(cli, child)

    pos = graphviz_layout(G_ssp, prog="dot")

    max_x = 0
    max_y = 0
    for key in pos:
        pos[key] = list(pos[key])

        if max_x < pos[key][0]:
            max_x = pos[key][0]
        if max_y < pos[key][1]:
            max_y = pos[key][1]

    return NetworkResponse(dict(pos), list(G_ssp.nodes),
                           dict(G_ssp.edges.keys()), max_x, max_y)
