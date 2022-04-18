
def collect_roots(node_level_data, level):
  roots = []

  for key in node_level_data.keys():
    node = node_level_data[key]

    level_id = int(node[0])

    if level != level_id:
     continue

    roots.append(node[2])

  return roots