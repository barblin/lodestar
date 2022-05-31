import json

from flask import Blueprint
from flask import request
from flask_apispec import doc
from flask import request
from flask import send_file
from services.export_service import export_file
import requests

from config.config import import_location

file_controller = Blueprint('file_controller', __name__)


@doc(tags=['files'])
@file_controller.route('/api/v1/downloads', methods=['POST'])
def downloads():
  data = request.get_json()
  url = data['url']
  name = url.split("/")[-1]
  r = requests.get(url, allow_redirects=True)
  open(import_location() + name, 'wb').write(r.content)
  return json.dumps({'filename': name})


@doc(tags=['files'])
@file_controller.route('/api/v1/exports/<filename>', methods=['GET'])
def export(filename):
  return send_file(export_file(filename, request.args.get('level'),
                               request.args.get('alpha')),
                   as_attachment=True)
