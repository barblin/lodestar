import json

from flask import Blueprint
from flask import Response
from flask import request

from services.label_service import get_labels, get_labels_all

label_controller = Blueprint('label_controller', __name__)


@label_controller.route('/api/v1/labels', methods=['POST'])
def labels():
  data = request.get_json()
  level = data["level"]
  alpha = data["alpha"]
  return Response(json.dumps(get_labels(level, alpha, data)),
                  mimetype='application/json')


@label_controller.route('/api/v1/labels/all', methods=['POST'])
def labels_all():
  data = request.get_json()
  return Response(json.dumps(get_labels_all(data)),
                  mimetype='application/json')
