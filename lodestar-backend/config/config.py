import os

knn_densities_ssp = [30, 50, 70, 90, 110, 130]

# feature scaling
v_scaling = 5
p_scaling = 1

# Tomato Ext settings
max_knn = 70
max_neighbors = 100
beta = 0.99
knn_cluster_graph = 30
knn_hypotest = 20
density_lower_limit = 15
density_upper_limit = 50
density_step_size = 2
levels = int((density_upper_limit - density_lower_limit) / density_step_size)


alpha_values = [0.05,
                0.025,
                0.0123,
                0.00625,
                0.003125,
                0.0015625,
                0.00078125]

dir_path = os.path.dirname(os.path.realpath(__file__))

resource_dir = dir_path + '/../resources/'

level_dir = '/levels/'
session_dir = '/sessions/'
export_dir = '/export/'
import_dir = '/import/'
alpha_dir = '/alphas/'

# COLUMNS
COL_LABEL = 'labels'
COL_CUSTOM_LABEL = 'custom_label'
COL_CUSTOM_LABEL_NAME = 'custom_label_name'


def get_alpha_array():
    return alpha_values


def alpha_location(alpha):
    return resource_dir + str(alpha)


def level_location(alpha):
    return alpha_location(alpha) + level_dir


def session_location(alpha):
    return alpha_location(alpha) + session_dir


def export_location():
    return resource_dir + export_dir


def import_location():
    return resource_dir + import_dir
