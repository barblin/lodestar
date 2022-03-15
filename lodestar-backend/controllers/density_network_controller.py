import json

from flask import Blueprint
from flask import Response
from flask import request

from services.network_service import produce_join_trees, get_current_tree, \
  get_trees, \
  get_significant_roots

network_controller = Blueprint('network_controller', __name__)


@network_controller.route('/api/v1/trees/<filename>', methods=['POST'])
def post_join_trees(filename):
  return Response("", mimetype='application/json')
  # data_axes = request.get_json()
  # produce_join_trees(filename, data_axes)
  # return Response("", mimetype='application/json')


@network_controller.route('/api/v1/trees/current', methods=['POST'])
def get_join_tree():
  data = request.get_json()
  print(data)
  return Response(get_current_tree(data), mimetype='application/json')


@network_controller.route('/api/v1/trees', methods=['GET'])
def get_join_trees():
  return Response(json.dumps(get_trees()), mimetype='application/json')


@network_controller.route('/api/v1/trees/significant/roots', methods=['GET'])
def get_sig_roots():
  roots = get_significant_roots()
  return Response(json.dumps(list(roots)), mimetype='application/json')
