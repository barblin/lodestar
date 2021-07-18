import itertools
import numpy as np
from sklearn.neighbors import kneighbors_graph
import networkx as nx
from numba import jit



@jit(nopython=True)
def uf_find(i, parents):
    """
    Find function for Union-Find data structure.

    Parameters:
        i (int): ID of point for which parent is required.
        parents (numpy array of shape (num_points)): array storing parents of each point.
    """
    if parents[i] == i:
        return i
    else:
        return uf_find(parents[i], parents)


@jit(nopython=True)
def uf_union(i, j, parents, f):
    """
    Union function for Union-Find data structure. Peak of smaller function value is attached to peak of larger function value.

    Parameters:
        i (int): ID of first point to be merged.
        j (int): ID of second point to be merged.
        parents (numpy array of shape (num_points)): array storing parents of each point.
        f (numpy array of shape (num_points)): array storing function values of each point.
    """
    if f[i] > f[j]:
        parents[j] = i
    else:
        parents[i] = j


class MergeGraph:
    def __init__(self, k_neighbors: int):
        """Constructor for fast mode finding class
            X:
            k_neighbors (int): number of neighbors used to build nearest neighbor graph (default None)

            Returns
            labels: clustering labels computed after calling fit() method.
        """
        self.k_neighbors = k_neighbors

        # Storage for merge-sequence and labels
        self.merge_sequence = None
        self.labels = None
        self.G = None  # directed graph object

    def build_adjacency_matrix(self, X):
        """Get adjacency matrix of knn graph with k_neighbors (member var)"""
        A = kneighbors_graph(X, n_neighbors=self.k_neighbors, include_self=False)
        A = A + A.T  # symmetrize matrix
        A[A.nonzero()] = 1  # setting >1 values to 1
        return A

    @staticmethod
    @jit(nopython=True)
    def fit_jit(density, a_indices, a_indptr):
        """
        Fit ModeFinder density a point cloud
        Parameters:
            density: input densities with same number of points as adjacency matrix
            a_indices: indices of sparse array
            a_indpts: index pointer of sparse array
            tau: merge parameter
        """
        num_pts = density.shape[0]
        parents = -np.ones(num_pts, dtype=np.int32)
        parents_unionized = -np.ones(num_pts, dtype=np.int32)

        # Prepare density
        sorted_idxs = np.flip(np.argsort(density))  # Sort indices by density
        inv_sorted_idxs = np.arange(num_pts)  # Mapping from index to density rank; lower index -> higher density
        for i in range(num_pts):
            inv_sorted_idxs[sorted_idxs[i]] = i

        merge_sequence = list()
        merge_sequence_full = list()
        # Graph which keeps the edge and node information: important for connected components function
        # Start Mode finding
        for i in range(num_pts):

            current_pt = sorted_idxs[i]  # loop through points in decreasing density fashion
            neighbors = a_indices[a_indptr[current_pt]:a_indptr[
                current_pt + 1]]  # get neighbor indices from (knn or radius neighbor) graph
            # Save neighbors with higher density
            higher_neighbors = [n for n in neighbors if inv_sorted_idxs[n] <= i]

            if len(higher_neighbors) == 0:  # if point has no neighbors with higher densities it is considered a new peak
                parents[current_pt] = current_pt  # in this case, a point is it's own parent
                parents_unionized[current_pt] = current_pt

            else:  # if a point has neighbors with higher densities
                # attribute point to neighbor with highest denisty
                g = higher_neighbors[np.argmax(density[np.array(higher_neighbors)])]  # highest density neighbor
                pg = uf_find(g, parents)  # parent = respective modal point of cluster
                pg_unionized = uf_find(g, parents_unionized)  # parent = respective modal point of cluster
                parents[current_pt] = pg  # add mode point to points info
                parents_unionized[current_pt] = pg_unionized

                # IF we are in a density well, i.e. all neigbors have a higher density (not some of them)
                # if len(higher_neighbors) == neighbors.shape[0]:
                # Loop through all neighbors with higher density than point "current_pt"

                # Get list of unionized parents -> connect only to parents which are not already merged
                higher_neighbors = np.array(higher_neighbors)
                neighboring_modes = np.array([uf_find(neighbor, parents) for neighbor in higher_neighbors])
                neighboring_modes_unionized = np.array(
                    [uf_find(neighbor, parents_unionized) for neighbor in higher_neighbors])
                higher_neighbors_new = []
                for un_id in set(neighboring_modes_unionized):
                    higher_neighbors_new.append(
                        higher_neighbors[np.argmin(density[neighboring_modes[neighboring_modes_unionized == un_id]])])

                prev_neighbors = list()
                for neighbor in higher_neighbors_new:
                    # HERE: we check if the valley between two peaks has a smaller prominence than tau,
                    # if so we merge then peaks

                    # Get modal point to which the neighbor point belongs to
                    pn = uf_find(neighbor, parents)
                    pn_unionized = uf_find(neighbor, parents_unionized)

                    # test if we already unionized them with the previous neighbors (previous i's)
                    already_unionized = False
                    if len(prev_neighbors) > 0:
                        for prev_nb in prev_neighbors:
                            parent_previous = uf_find(prev_nb, parents_unionized)
                            if pn_unionized == parent_previous:
                                already_unionized = True
                    # Store previous parents in list
                    prev_neighbors.append(neighbor)

                    # If another member from the upper star of a point does not follow the gradient towards
                    # the same points as pg then we add a direct path over the point current_pt between pn and pg
                    if (pn != pg) and (not already_unionized):
                        if density[pg_unionized] > density[pn_unionized]:
                            merge_sequence.append([
                                pn, pg,  # Path connecting the following peaks
                                current_pt,  # Saddle point in between
                                density[pn] - density[current_pt],  # Density difference/cost downhill to saddle
                                density[pg] - density[current_pt]  # Density difference/cost uphill from saddle
                            ])
                            # Full merge sequence history with actual merging
                            merge_sequence_full.append((i, pn, pg_unionized))

                            # ---- unionize  -----
                            uf_union(pg_unionized, pn_unionized, parents_unionized, density)

                        elif density[pg_unionized] < density[pn_unionized]:  # and (pg not in already_merged_peaks):
                            merge_sequence.append([
                                pg, pn,  # Path connecting the following peaks
                                current_pt,  # Saddle point in between
                                density[pg] - density[current_pt],  # Density difference/cost downhill to saddle
                                density[pn] - density[current_pt]  # Density difference/cost uphill from saddle
                            ])
                            # Full merge sequence history with actual merging
                            merge_sequence_full.append((i, pg, pn_unionized))

                            # ---- unionize  -----
                            uf_union(pg_unionized, pn_unionized, parents_unionized, density)

        # labels = id of mode point where each individual point ends up
        labels = np.array([uf_find(n, parents) for n in range(num_pts)])
        # Remove duplicate entries
        return merge_sequence, labels, merge_sequence_full

    def fit(self, X: np.ndarray, density: np.ndarray):
        """Fit data with given density"""
        if density.shape[0] != X.shape[0]:
            raise ValueError('Shape mismatch between input density and data!')

        # Build adjacency matrix
        A = self.build_adjacency_matrix(X)
        # Fit
        ms, self.labels, ms_full = self.fit_jit(density, A.indices, A.indptr)
        # Merge sequence post processing
        ms.sort()
        merge_sequence_graph = [ums for ums, _ in itertools.groupby(ms)]

        ms_full.sort()
        self.merge_sequence = [ums for ums, _ in itertools.groupby(ms_full)]

        # create directed graph
        self.G = self.build_graph(merge_sequence_graph)

        self.merge_sequence = self.build_merge_sequence(density)

        return self.G, self.labels, self.merge_sequence

    def build_graph(self, merge_sequence):
        """Loop through merge sequence and insert edges into directed graph"""
        tmp_g = nx.Graph()  # instantiate directed graph
        for ms in merge_sequence:
            # ms[0]...peak 1
            # ms[1]...peak 2
            # ms[3]+ms[4]...density difference between peaks
            # tmp_g.add_edge(ms[0], ms[1], weight=ms[3]+ms[4])
            tmp_g.add_edge(ms[0], ms[2])
            tmp_g.add_edge(ms[2], ms[1])
        return tmp_g

    def build_merge_sequence(self, density):
        merge_sequence_final = list()
        nodes_idx = np.array(self.G.nodes, dtype=int)
        num_pts = nodes_idx.size
        density_nodes = density[nodes_idx]
        parents = -np.ones(density.size, dtype=np.int32)
        # Prepare density
        sorted_idxs = np.flip(np.argsort(density_nodes))  # Sort indices by density

        # Graph which keeps the edge and node information: important for connected components function
        # Start Mode finding
        for i in range(num_pts):
            current_pt = nodes_idx[sorted_idxs[i]]  # loop through points in decreasing density fashion
            neighbors = [int(n) for n in self.G.neighbors(current_pt)]
            # Save neighbors with higher density
            higher_neighbors = [n for n in neighbors if density[n] > density[current_pt]]

            if len(higher_neighbors) == 0:  # point is new peak
                parents[current_pt] = current_pt  # in this case, a point is it's own parent
            else:  # if a point has neighbors with higher densities
                # attribute point to neighbor with highest density
                g = higher_neighbors[np.argmax(density[np.array(higher_neighbors)])]  # highest density neighbor
                pg = uf_find(g, parents)  # parent = respective modal point of cluster
                parents[current_pt] = pg  # add mode point to points info
                for neigh in higher_neighbors:
                    # Get modal point to which the neighbor point belongs to
                    pn = uf_find(neigh, parents)
                    if (pn != pg) and (neigh != pg):
                        # merge_sequence_final.append([i, pn, pg])
                        merge_sequence_final.append([i, neigh, pg])
                        # ---- unionize  -----
                        uf_union(pg, pn, parents, density)
        return merge_sequence_final