from config.config import max_knn, max_neighbors, beta, knn_cluster_graph, \
    knn_hypotest, alpha
from core.Modality.TomatoExtension import TomatoExtension


def create_graph(df_cluster):
    tomato = TomatoExtension(df_cluster, max_neighbors=max_neighbors, beta=beta,
                             knn_cluster_graph=knn_cluster_graph,
                             knn_hypotest=knn_hypotest, knn_max=max_knn)
    tomato.update(knn_hypotest=knn_hypotest, knn_cluster_graph=40)
    return tomato.fit(alpha=alpha), tomato
