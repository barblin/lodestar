import json


class NetworkResponse:
  def __init__(self, pos, nodes, node_level_clusters, edges, max_x, max_y,
      max_nodes):
    self.pos = pos
    self.nodes = nodes
    self.node_level_clusters = node_level_clusters
    self.edges = edges
    self.max_x = max_x + 20
    self.max_y = max_y + 20
    self.max_nodes = max_nodes

  def jsonify(self):
    return json.dumps(self.__dict__)
