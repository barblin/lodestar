import os

knn_densities_ssp = [30, 50, 70, 90, 110, 130]

# feature scaling
v_scaling = 5
p_scaling = 1

# Tomato Ext settings
max_knn = 70
max_neighbors = 100
beta = 0.99
knn_cluster_graph = 50
knn_hypotest = 20
alpha = 0.05

alpha_values = [0.05,
                0.01,
                0.001]

dir_path = os.path.dirname(os.path.realpath(__file__))
level_dir = dir_path + '/../resources/levels/'
session_dir = dir_path + '/../resources/sessions/'
export_dir = dir_path + '/../resources/export/'

# COLUMNS
COL_LABEL = "labels"
COL_CUSTOM_LABEL = "custom_label"
COL_CUSTOM_LABEL_NAME = "custom_label_name"


def level_location():
  return level_dir


def session_location():
  return session_dir


def export_location():
  return export_dir
