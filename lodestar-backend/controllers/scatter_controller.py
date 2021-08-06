import json

from flask import Blueprint

from services import scatter_service

scatter_controller = Blueprint('scatter_controller', __name__)


@scatter_controller.route('/api/v1/scatters/<filename>')
def scatters(filename):
    return json.dumps(scatter_service.get(filename))
