import json


class NetworkResponse:
    def __init__(self, pos, nodes, edges, max_x, max_y):
        self.pos = pos
        self.nodes = nodes
        self.edges = edges
        self.max_x = max_x + 20
        self.max_y = max_y + 20

    def jsonify(self):
        return json.dumps(self.__dict__)
