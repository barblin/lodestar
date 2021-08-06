from flask import Blueprint

cluster_controller = Blueprint('cluster_controller', __name__)


@cluster_controller.route('/api/v1/hello')
def cluster():
    return 'Hello World'
