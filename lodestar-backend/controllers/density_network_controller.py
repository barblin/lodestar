from flask import Blueprint

from services.network_service import get_join_tree

network_controller = Blueprint('network_controller', __name__)


@network_controller.route('/api/v1/networks/<filename>')
def resources(filename):
    return get_join_tree(filename).jsonify()
