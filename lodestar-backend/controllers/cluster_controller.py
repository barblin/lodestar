import json

from flask import Blueprint
from flask import Response
from flask import request

from services.cluster_service import update_cluster as update
from flask_apispec import doc

cluster_controller = Blueprint('cluster_controller', __name__)


@cluster_controller.route('/api/v1/levels/<lid>/cluster/<cid>',
                          methods=['POST'])
@doc(tags=['clusters'])
def update_cluster(lid, cid):
  data = request.get_json()
  return Response(json.dumps(update(lid, cid, data)),
                  mimetype='application/json')
