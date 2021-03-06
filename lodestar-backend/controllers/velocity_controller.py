import json

from flask import Blueprint
from flask import Response
from flask import request
from flask_apispec import doc

from services.velocity_service import get_velocity

velocity_controller = Blueprint('velocity_controller', __name__)


@doc(tags=['velocity'])
@velocity_controller.route('/api/v1/velocity/<filename>', methods=['POST'])
def velocity(filename):
  data = request.get_json()
  return Response(json.dumps(get_velocity(filename, data)),
                  mimetype='application/json')
