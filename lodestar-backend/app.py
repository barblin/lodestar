from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec

from config.docs import register
from controllers.cluster_controller import cluster_controller
from controllers.network_controller import network_controller
from controllers.file_controller import file_controller
from controllers.heatmap_controller import heatmap_controller
from controllers.hrd_controller import hrd_controller
from controllers.label_controller import label_controller
from controllers.resource_controller import resource_controller
from controllers.space_controller import space_controller
from controllers.velocity_controller import velocity_controller

app = Flask(__name__)

app.register_blueprint(space_controller)
app.register_blueprint(velocity_controller)
app.register_blueprint(label_controller)
app.register_blueprint(resource_controller)
app.register_blueprint(network_controller)
app.register_blueprint(hrd_controller)
app.register_blueprint(cluster_controller)
app.register_blueprint(heatmap_controller)
app.register_blueprint(file_controller)

spec = APISpec(
    title='clusters',
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
docs = FlaskApiSpec(app)
register(docs)


@app.route("/")
def hello():
  return "Service running"


@app.after_request
def after_request(response):
  header = response.headers
  header['Access-Control-Allow-Origin'] = '*'
  header['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
  header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
  return response


if __name__ == "__main__":
  app.run(host='0.0.0.0', threaded=True)
