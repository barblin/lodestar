import json

from flask import Blueprint
from flask import Response
from flask_apispec import doc

from services.heatmap_service import get_heatmap

heatmap_controller = Blueprint('heatmap_controller', __name__)


@doc(tags=['heatmap'])
@heatmap_controller.route('/api/v1/heatmap', methods=['GET'])
def heatmap():
  return Response(json.dumps(get_heatmap()), mimetype='application/json')
