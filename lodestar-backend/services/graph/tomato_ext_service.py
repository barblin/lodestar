from config.config import max_knn, max_neighbors, beta, knn_cluster_graph, \
    knn_hypotest
from core.Modality.SigMA import SigMA


def create_graph(df_cluster, alpha):
    tomato = SigMA(df_cluster, max_neighbors=max_neighbors, beta=beta,
                             knn_initcluster_graph=knn_cluster_graph,
                             knn_hypotest=knn_hypotest)
    tomato.update(knn_hypotest=knn_hypotest, knn_initcluster_graph=40)
    print(alpha)
    return tomato.fit(alpha=alpha), tomato
