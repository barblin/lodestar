import json

from flask import Blueprint
from flask import Response
from flask import request
from flask_apispec import doc

from services.space_service import get_space

space_controller = Blueprint('space_controller', __name__)


@doc(tags=['space'])
@space_controller.route('/api/v1/space/<filename>', methods=['POST'])
def space(filename):
    data = request.get_json()
    return Response(json.dumps(get_space(filename, data)),
                    mimetype='application/json')
