
def collect_roots(node_level_data):
  collection = {}
  highest_id = 0

  for key in node_level_data.keys():
    node = node_level_data[key]

    level_id = int(node[0])

    if highest_id < level_id:
     highest_id = level_id

    cluster = node[2]

    if level_id in collection.keys():
      entry = collection[level_id]
      entry.append(cluster)
      collection[level_id] = entry
    else:
      collection[level_id] = [cluster]

  return collection[highest_id]