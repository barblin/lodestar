from controllers.cluster_controller import update_cluster
from controllers.network_controller import post_join_trees, \
  get_join_tree, get_join_trees, get_sig_roots
from controllers.file_controller import downloads, export
from controllers.heatmap_controller import heatmap
from controllers.hrd_controller import hrd
from controllers.label_controller import labels, labels_all
from controllers.resource_controller import resources, alpha_levels, \
  density_levels, resource_headers
from controllers.space_controller import space
from controllers.velocity_controller import velocity


def register(docs):
  docs.register(space, blueprint="space_controller")
  docs.register(velocity, blueprint="velocity_controller")
  docs.register(labels, blueprint="label_controller")
  docs.register(labels_all, blueprint="label_controller")
  docs.register(resources, blueprint="resource_controller")
  docs.register(alpha_levels, blueprint="resource_controller")
  docs.register(density_levels, blueprint="resource_controller")
  docs.register(resource_headers, blueprint="resource_controller")
  docs.register(post_join_trees, blueprint="network_controller")
  docs.register(get_join_tree, blueprint="network_controller")
  docs.register(get_join_trees, blueprint="network_controller")
  docs.register(get_sig_roots, blueprint="network_controller")
  docs.register(hrd, blueprint="hrd_controller")
  docs.register(update_cluster, blueprint="cluster_controller")
  docs.register(heatmap, blueprint="heatmap_controller")
  docs.register(downloads, blueprint="file_controller")
  docs.register(export, blueprint="file_controller")

  for key, value in docs.spec._paths.items():
    docs.spec._paths[key] = {
      inner_key: inner_value
      for inner_key, inner_value in value.items()
      if inner_key != 'options'
    }
