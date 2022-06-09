import json

from config.config import alpha_values, levels
from services.data.tree_source import get_tree
from services.significant_roots_service import collect_roots


def get_heatmap():
  heatmap_cells = calculate_heatmap()
  alpha_histo, a_min, a_max = compute_alpha_hist(heatmap_cells)
  density_histo, d_min, d_max = compute_density_hist(heatmap_cells)

  heatmap = []
  max_value = 0
  min_value = 10000000

  alpha_counter = 0
  for alpha in heatmap_cells:
    density_counter = 0
    for density in heatmap_cells[alpha]:
      sum = int(heatmap_cells[alpha][density])
      if sum < min_value:
        min_value = sum

      if max_value < sum:
        max_value = sum

      heatmap.append(
          {"group": str(density_counter),
           "variable": "α " + str(alpha_counter),
           "value": sum,
           "alpha": alpha_values[int(alpha)],
           "level": density})

      density_counter += 1

    alpha_counter += 1

  cluster, domain, cmax = get_cluster_for_alpha_and_density()

  return {"heatmap": heatmap, "max_value": max_value, "min_value": min_value,
          'alpha_histo': alpha_histo, 'amin': a_min, 'amax': a_max,
          'density_histo': density_histo, 'dmin': d_min, 'dmax': d_max,
          'cluster': cluster, 'domain': domain, 'cmax': cmax}


def compute_density_hist(denisty_map):
  histo = []
  min_value = 1000000
  max_value = 0

  for a_key in denisty_map.keys():
    sum = 0
    for d_key in denisty_map[a_key]:
      sum += denisty_map[a_key][d_key]

    if sum < min_value:
      min_value = sum

    if max_value < sum:
      max_value = sum
    histo.append(sum)

  return histo, min_value, max_value


def compute_alpha_hist(alpha_map):
  histo = []
  min_value = 1000000
  max_value = 0

  for i in range(0, levels+1):
    sum = 0
    for a_key in alpha_map.keys():
      sum += alpha_map[a_key][i]

    if sum < min_value:
      min_value = sum

    if max_value < sum:
      max_value = sum
    histo.append(sum)

  return histo, min_value, max_value


def get_cluster_for_alpha_and_density():
  cluster = []
  domain = []
  cmax = 0

  for i in range(0, len(alpha_values)):
    tree = alpha_values[i]

    left_tree = json.loads(get_tree(str(tree)))

    for level in range(0, levels+1):
      clusters = collect_roots(left_tree["node_level_clusters"], level)

      domain.append("α " + str(i) + "," + "d " + str(level))

      num_cluster = len(clusters)
      cluster.append({'num_cluster': num_cluster, 'level': level, 'alpha': alpha_values[i]})

      if cmax < num_cluster:
        cmax = num_cluster

  return cluster, domain, cmax


def calculate_heatmap():
  heatmap = {}
  alpha_trees = {}

  for i in range(0, len(alpha_values)):
    for level in range(0, levels+1):
      amount = 0
      difference = 0

      current = get_clusters(alpha_trees, i, level)

      if (i + 1) < len(alpha_values):
        top = get_clusters(alpha_trees, i + 1, level)
        difference += len(set(current).symmetric_difference(set(top)))
        amount += 1

      if 0 <= (i - 1):
        bottom = get_clusters(alpha_trees, i - 1, level)
        difference += len(set(current).symmetric_difference(set(bottom)))
        amount += 1

      if (level + 1) < levels + 1:
        right = get_clusters(alpha_trees, i, level + 1)
        difference += len(set(current).symmetric_difference(set(right)))
        amount += 1

      if 0 <= (level - 1):
        left = get_clusters(alpha_trees, i, level - 1)
        difference += len(set(current).symmetric_difference(set(left)))
        amount += 1

      if str(i) in heatmap.keys():
        entry = heatmap[str(i)]
      else:
        entry = {}

      entry[level] = difference / amount
      heatmap[str(i)] = entry

  return heatmap


def get_clusters(alpha_trees, i, level):
  if str(i) in alpha_trees.keys():
    return collect_roots(alpha_trees[str(i)], level)
  else:
    alpha_trees[str(i)] = json.loads(get_tree(str(alpha_values[i])))[
      "node_level_clusters"]

    return collect_roots(alpha_trees[str(i)], level)
