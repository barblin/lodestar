import numpy as np
from scipy.spatial import Delaunay, cKDTree
from scipy.sparse import csr_matrix


def build_gabriel_graph_from_delaunay(X, tri, delaunay_adjacency_matrix):
    """Remove edges from delaunay triangulation and returns the adjaceny matrix of a Gabriel graph
    :param delaunay_adjacency_matrix: scipy sparse matrix (csr format)
    """
    # Convert adjacency matrix to coo format for direct access to each node-edge-node pair
    coo = delaunay_adjacency_matrix.tocoo()
    # edge_idx contains the index of 2 nodes at each end of an edge
    delaunay_edge_indices = np.vstack((coo.row, coo.col)).T
    # Sort cols
    delaunay_edge_indices = np.sort(delaunay_edge_indices, axis=1)
    # ---- Trim Edges from Delaunay tessellation to get Gabriel graph ----
    # Find centroid or midpoint of each edge in conns
    c = tri.points[delaunay_edge_indices]
    m = (c[:, 0, :] + c[:, 1, :]) / 2  # midpoint of each edge in graph
    # Find the radius sphere between each pair of nodes
    r = np.sqrt(np.sum((c[:, 0, :] - c[:, 1, :]) ** 2, axis=1)) / 2
    # Use the kd-tree function in Scipy's spatial module & find the nearest point for each midpoint
    n = cKDTree(X).query(x=m, k=1)[0]
    # If nearest point to m is at a distance r, then the edge is a Gabriel edge
    g = n >= (r * 0.999)  # The factor is to avoid precision errors in the distances
    # Reduce the connectivity to all True values found in g
    row_ind, col_ind = delaunay_edge_indices[g].T
    # Construct sparse adjacency matrix
    adj_gabriel = csr_matrix((np.ones_like(row_ind), (row_ind, col_ind)), shape=(tri.npoints, tri.npoints))
    return adj_gabriel


def gabriel_graph_adjacency(X: np.ndarray):
    # Create delaunay triangulation & from that Gabriel graph
    tri = Delaunay(points=X)
    indptr, indices = tri.vertex_neighbor_vertices  # get index pointer and indices for sparse csr matrix
    delaunay_adj_mtx = csr_matrix((np.ones_like(indices), indices, indptr), shape=(tri.npoints, tri.npoints))
    return build_gabriel_graph_from_delaunay(X, tri, delaunay_adj_mtx)

