import json

from flask import Blueprint
from flask import Response
from flask import request

from services.network_service import get_current_tree, \
  get_trees, \
  get_significant_roots, produce_join_trees

network_controller = Blueprint('network_controller', __name__)


@network_controller.route('/api/v1/trees/<filename>', methods=['POST'])
def post_join_trees(filename):
  return Response("", mimetype='application/json')
  #data_axes = request.get_json()
  #produce_join_trees(filename, data_axes)
  #return Response("", mimetype='application/json')


@network_controller.route('/api/v1/trees/current', methods=['POST'])
def get_join_tree():
  data = request.get_json()
  return Response(get_current_tree(data), mimetype='application/json')


@network_controller.route('/api/v1/trees', methods=['GET'])
def get_join_trees():
  return Response(json.dumps(get_trees()), mimetype='application/json')


@network_controller.route('/api/v1/trees/significant/roots', methods=['POST'])
def get_sig_roots():
  data = request.get_json()
  roots = get_significant_roots(data)
  return Response(json.dumps(roots), mimetype='application/json')
