import numpy as np
from miscellaneous.utils import pairwise_loop
from LineGeometry.utils import distance
from scipy.spatial import cKDTree
from Sampler.PerturbData import PerturbedData
import time


def point_along_direction_precomputed_dista2b(a, b, travel_dist, dist_a2b):
    # unit vector
    unit_vector = ((b - a) / dist_a2b).reshape((1, a.size))
    return a + travel_dist.reshape(travel_dist.size, 1) @ unit_vector


class GraphPreprocessing:
    """Create n resampled data sets (ds): each group is a different resampled ds
       Store for each edge a list of distances to the n'th neighbor
    """
    def __init__(self, data, df_cluster, labels, G, velocity_scale, nb_neighbors, step_size, nb_resample_ds=10):
        self.nb_neighbors = nb_neighbors
        self.step_size = step_size
        self.nb_resample_ds = nb_resample_ds
        self.velocity_scale = velocity_scale
        self.perturbed_data_inst = PerturbedData(data)
        self.perturbed_data_inst.build_covariance_matrix()
        print('Distance dictionary...')
        st = time.time()
        self.dist_dict = self.create_dist_dict(df_cluster, G, labels)
        print(f'Done!  [took {time.time()-st:.2f} sec')

    def create_dist_dict(self, data, G, labels):
        data_idx = np.arange(data.shape[0])
        # Dictionary containing distance information for modality test
        dist_dict = dict()
        for i in range(self.nb_resample_ds + 1):
            if i > 0:
                # Sample from gaussian covariance matrix centered on data point
                print('Resampling data & building kdTree...')
                X_new = self.perturbed_data_inst.new_sample()
                data_resampled = self.perturbed_data_inst.change_coordinates(X_new)
                data_resampled[['v_alpha', 'v_delta']] *= self.velocity_scale
                kd_tree = cKDTree(data=data_resampled)
                print('Done!')
                current_data = data_resampled
            else:
                # Create KD tree for fast distance calculation
                print('Creating kdTree...')
                kd_tree = cKDTree(data=data)
                current_data = data
                print('Done!')

            for e in G.edges:
                data_set_name = f'e{min(e)}-e{max(e)}'  # ordered, so that lowest edge number comes first
                edge_sorted = np.asarray(sorted(e))

                x_begin, x_end = current_data.iloc[edge_sorted].values
                # Interpolate path in max_step increments
                dist = distance(x_begin, x_end)
                inbetween_pts = point_along_direction_precomputed_dista2b(
                    x_begin, x_end, np.arange(1, int(dist // self.step_size) + 1) * self.step_size, dist
                )
                interpol = np.vstack([x_begin, inbetween_pts, x_end])
                # Query kdTree and compute distance to k'th neighbor
                d_knn, _ = kd_tree.query(interpol, k=self.nb_neighbors, n_jobs=-1)
                d_knn = np.max(d_knn, axis=1)

                # update modal point caused by resampling
                # The track should start and end then from the new modal points

                # 1 of edges is a mode, the other is a saddle point/valley -> we only modify the modal position
                # modal_point_to_resample = np.intersect1d(labels, edge_sorted)  # returns numpy array
                # if modal_point_to_resample.size > 1:
                #     msg = f"Two modes next to each other without a saddle point in between: edge {edge_sorted}"
                #     raise ValueError(msg)
                # if i > 0:
                #     # Since we resample the data set the initially defined modes
                #     # might no longer be centered on the same point.
                #     # Therefore, we find the new mode and more importantly the distances to its nb_neighbors.
                #     # They represent the first and last portions of the path
                #     is_old_mode = labels == modal_point_to_resample[0]
                #     d_knn_old_mode, _ = kd_tree.query(current_data.loc[is_old_mode], k=self.nb_neighbors, n_jobs=-1)
                #
                #     # ----------- Version A: update modal point in first and last "cluster" --------------
                #     # new_mode_arg = np.argmin(np.max(d_knn_old_mode, axis=1))
                #     # new_mode_idx = data_idx[is_old_mode][new_mode_arg]
                #     # Update edge sorted
                #     # edge_sorted[edge_sorted == modal_point_to_resample[0]] = new_mode_idx
                #
                #     # --------- Version B: we just substitute the first and last distance with the densest one -------
                #     # New mode: Mode = minimum distance of point to it's neighbors
                #     d_mode = np.min(np.max(d_knn_old_mode, axis=1))
                # else:
                #     # We too save the distance of the to the k'th nn for the original data set
                #     if np.sum(np.arange(2)[edge_sorted == modal_point_to_resample[0]]) == 0:
                #         # The mode is the "lower number" mode
                #         d_mode = d_knn[0]
                #     else:
                #         # The mode is the "higher number" mode
                #         d_mode = d_knn[-1]

                # instead of d_knn, we might just have to save np.max(d_knn),
                # since we only need to know if one of the values is dipping under the "alpha line"
                if data_set_name in dist_dict:
                    # dist_dict[data_set_name].append({'distances': d_knn, 'mode': d_mode})
                    dist_dict[data_set_name].append(d_knn)
                else:
                    # dist_dict[data_set_name] = [{'distances': d_knn, 'mode': d_mode}]
                    dist_dict[data_set_name] = [d_knn]
        return dist_dict

    def get_distances_along_path(self, path):
        all_paths = []
        all_d_modes = []
        for i in range(self.nb_resample_ds + 1):
            distances_path = []
            for j, (first, last) in enumerate(pairwise_loop(path)):
                edge = sorted([first, last])
                # Modes along the path
                # d_mode_i = self.dist_dict[f'e{min(edge)}-e{max(edge)}'][i]['mode']
                # all_d_modes.append(d_mode_i)
                # Distances to k'th nearest neighbor along the path
                dist_i = self.dist_dict[f'e{min(edge)}-e{max(edge)}'][i]
                # dist_i = self.dist_dict[f'e{min(edge)}-e{max(edge)}'][i]['distances']

                if first > last:
                    dist_i = dist_i[::-1]
                # The points overlap on each end (end of one, start of next):
                #   we remove the start except for the first one
                if j == 0:
                    # insert the full
                    distances_path.append(dist_i)
                else:
                    distances_path.append(dist_i[1:])
            all_paths.append(np.concatenate(distances_path))
        return all_paths  #, all_d_modes
