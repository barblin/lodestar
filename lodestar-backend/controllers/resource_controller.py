import json

from flask import Blueprint

from services import resource_service

resource_controller = Blueprint('resource_controller', __name__)


@resource_controller.route('/api/v1/resources')
def resources():
    return json.dumps(resource_service.list_content())
