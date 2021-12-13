from flask import Blueprint
from flask import request

from services.network_service import get_join_tree

network_controller = Blueprint('network_controller', __name__)


@network_controller.route('/api/v1/networks/<filename>', methods=['POST'])
def resources(filename):
    data_axes = request.get_json()
    return get_join_tree(filename, data_axes).jsonify()
