import json

from flask import Blueprint
from flask_apispec import doc

from config.config import knn_densities_ssp, alpha_values
from services.data import resource_service

resource_controller = Blueprint('resource_controller', __name__)


@doc(tags=['configurations'])
@resource_controller.route('/api/v1/resources', methods=['GET'])
def resources():
  return json.dumps(resource_service.list_content())


@doc(tags=['configurations'])
@resource_controller.route('/api/v1/alphas', methods=['GET'])
def alpha_levels():
  return json.dumps(alpha_values)


@doc(tags=['configurations'])
@resource_controller.route('/api/v1/density-levels', methods=['GET'])
def density_levels():
  return json.dumps(knn_densities_ssp)


@doc(tags=['configurations'])
@resource_controller.route('/api/v1/resources/<filename>/headers',
                           methods=['GET'])
def resource_headers(filename):
  return json.dumps(resource_service.get_resource_headers(filename))
