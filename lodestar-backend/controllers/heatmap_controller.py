import json

from flask import Blueprint
from flask import Response

from services.heatmap_service import get_heatmap

heatmap_controller = Blueprint('heatmap_controller', __name__)


@heatmap_controller.route('/api/v1/heatmap', methods=['GET'])
def heatmap():
  return Response(json.dumps(get_heatmap()), mimetype='application/json')
