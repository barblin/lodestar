import json

from flask import Blueprint
from flask import Response
from flask import request

from services.label_service import get_labels

label_controller = Blueprint('label_controller', __name__)


@label_controller.route('/api/v1/labels/<filename>', methods=['POST'])
def labels(filename):
  data = request.get_json()
  return Response(json.dumps(get_labels(filename, data)),
                  mimetype='application/json')
