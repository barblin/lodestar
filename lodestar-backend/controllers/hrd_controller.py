import json

from flask import Blueprint
from flask import Response
from flask import request

from services.hrd_service import get_hrd

hrd_controller = Blueprint('hrd_controller', __name__)


@hrd_controller.route('/api/v1/hrd/<filename>', methods=['POST'])
def hrd(filename):
  data = request.get_json()
  print(data)
  return Response(json.dumps(get_hrd(filename, data)),
                  mimetype='application/json')
