import json

from flask import Blueprint
from flask import Response
from flask import request

from services.velocity_service import get_velocity, get_radial

velocity_controller = Blueprint('velocity_controller', __name__)


@velocity_controller.route('/api/v1/velocity/<filename>', methods=['POST'])
def velocity(filename):
  data = request.get_json()
  return Response(json.dumps(get_velocity(filename, data)),
                  mimetype='application/json')
