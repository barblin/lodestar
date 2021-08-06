from flask import Flask

from controllers.cluster_controller import cluster_controller
from controllers.network_controller import network_controller
from controllers.resource_controller import resource_controller
from controllers.scatter_controller import scatter_controller

app = Flask(__name__)

app.register_blueprint(cluster_controller)
app.register_blueprint(scatter_controller)
app.register_blueprint(resource_controller)
app.register_blueprint(network_controller)


@app.route("/")
def hello():
    return "Service running"


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
