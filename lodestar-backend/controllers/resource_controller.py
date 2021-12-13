import json

from flask import Blueprint
from flask import request
from flask import send_file

from config.config import knn_densities_ssp
from services.data import resource_service
from services.export_service import export_file

resource_controller = Blueprint('resource_controller', __name__)


@resource_controller.route('/api/v1/resources')
def resources():
    return json.dumps(resource_service.list_content())


@resource_controller.route('/api/v1/density-levels')
def density_levels():
    return knn_densities_ssp


@resource_controller.route('/api/v1/resources/<filename>/headers')
def resource_headers(filename):
    return json.dumps(resource_service.get_resource_headers(filename))


@resource_controller.route('/api/v1/exports/<filename>')
def export(filename):
    return send_file(export_file(filename, request.args.get('level')),
                     as_attachment=True)
