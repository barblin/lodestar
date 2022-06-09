import scipy
import numpy as np
# Specialized class for this situation
from sklearn.metrics.cluster import contingency_matrix


class SparseMatrixOperations:
    def __init__(self, sparse_matrix=None):
        self.A = sparse_matrix
        # keep also csr and coo matrix
        # -> faster for some operations to do in csr or coo format
        self.A_csr = None
        self.A_coo = None
        # set csr and coo matrices
        self._set_specific_matrices()

    def _set_specific_matrices(self):
        """Setters for A_csr, A_coo"""
        if self.A is not None:
            if isinstance(self.A, scipy.sparse.csr_matrix):
                self.A_csr = self.A
                self.A_coo = self.A.tocoo()

            elif isinstance(self.A, scipy.sparse.coo_matrix):
                self.A_csr = self.A.tocsr()
                self.A_coo = self.A

            else:
                self.A_csr = self.A.tocsr()
                self.A_coo = self.A.tocoo()

    def update(self, data_sparse, rows_sparse, cols_sparse, shape):
        """Update the sparse matrix stored in self.A"""
        self.A = scipy.sparse.csr_matrix((data_sparse, (rows_sparse, cols_sparse)), shape=shape)
        self._set_specific_matrices()

    def zero_rows_indices(self):
        """Return rows of matrix with all zeros"""
        return np.flatnonzero(np.diff(self.A_csr.indptr) == 0)

    def maximum(self):
        """Returns maximum value and row and column index"""
        k = self.A_coo.data.argmax()
        max_val = self.A_coo.data[k]
        max_row = self.A_coo.row[k]
        max_col = self.A_coo.col[k]
        return {'val': max_val, 'row': max_row, 'col': max_col}

    def set_row_to_val(self, row, value=0):
        """Set all nonzero elements in a given row to the given value.
        Useful to set to 0 mostly."""
        self.A_csr.data[self.A_csr.indptr[row]:self.A_csr.indptr[row + 1]] = value
        self.A_csr.eliminate_zeros()


# Specialized class for this situation
class IterativeMaxFinderSparse(SparseMatrixOperations):
    def __init__(self, sparse_matrix=None):
        super().__init__(sparse_matrix)

    def iterative_max(self):
        """Loop through the maximal values of the matrix:
            1) find overall maximal value (row and column) = find best fitting cluster match (might be multiple matches)
            2) store new cluster (row) - ClusterCollection of already existing cluster (column)
            3) set that column to 0
            4) if matrix has more nonzero entries, go back to 1, else break
        """
        row_column_info = list()
        while self.A_csr.count_nonzero() > 0:
            max_info = self.maximum()  # maximal value with row and column info
            # Remove row with maximal value (we want to match 1 cluster to 1 scale space cluster)
            self.set_row_to_val(max_info['row'], value=0)
            row_column_info.append(max_info)

        return row_column_info


class JaccardMatrix(SparseMatrixOperations):
    def __init__(self, label_set_rows, label_set_cols):
        """Input: 2 label sets with the same length"""
        if label_set_rows.shape != label_set_cols.shape:
            raise ValueError('Both label sets must have the same shape!')
        # Instantiate super class with contingency_matrix of label set 1 and 2
        super().__init__(contingency_matrix(label_set_rows, label_set_cols, sparse=True, eps=None))
        # set member variables
        self.label_set_rows = label_set_rows
        self.label_set_cols = label_set_cols
        self.unique_rows = np.unique(label_set_rows)  # contingency_matrix sorts unique values in ascending way
        self.unique_cols = np.unique(label_set_cols)
        # build jaccard matrix
        self._build_jaccard_matrix()

    def _build_jaccard_matrix(self):
        """Create sparse matrix with jaccard index of cluster i of label_set_rows and j of label_set_cols"""
        # Count the number of points each cluster id has for the first and second label set
        count_id_rows = {cl_id: count for cl_id, count in zip(*np.unique(self.label_set_rows, return_counts=True))}
        count_id_cols = {cl_id: count for cl_id, count in zip(*np.unique(self.label_set_cols, return_counts=True))}
        new_data = list()
        for i, j, data in zip(self.A_coo.row, self.A_coo.col, self.A_coo.data):
            # The contingency matrix stores the cardinality of the intersection between cluster A and B: |AuB|
            # To get the jaccard similarity:
            # we divide by the cardinality of the union of the clusters: |AnB| = |A| + |B| - |AuB|
            ci = count_id_rows[self.unique_rows[i]]
            cj = count_id_cols[self.unique_cols[j]]
            new_data.append(data / (ci + cj - data))
        # Update matrix with jaccard data (at the same position, so only data needs updating)
        self.update(data_sparse=new_data,
                    rows_sparse=self.A_coo.row,
                    cols_sparse=self.A_coo.col,
                    shape=self.A_coo.shape
                    )
        self._set_specific_matrices()

    def threshold_matrix(self, threshold: float):
        """Remove values from matrix less than threshold"""
        self.A_csr.data[self.A_csr.data < threshold] = 0
        self.A_csr.eliminate_zeros()
        self.A = self.A_csr
        self._set_specific_matrices()

    def nonzero_idx_pairs(self):
        """Returns a list of nonzero indices"""
        return [{'row': i, 'col': j, 'val': data} for i, j, data in
                zip(self.A_coo.row, self.A_coo.col, self.A_coo.data)]
