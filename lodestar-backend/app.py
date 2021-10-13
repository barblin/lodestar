from flask import Flask

from controllers.density_network_controller import network_controller
from controllers.resource_controller import resource_controller
from controllers.space_controller import space_controller
from controllers.velocity_controller import velocity_controller

app = Flask(__name__)

app.register_blueprint(space_controller)
app.register_blueprint(velocity_controller)
app.register_blueprint(resource_controller)
app.register_blueprint(network_controller)


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
    app.run(host='0.0.0.0')
