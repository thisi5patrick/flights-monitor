from flask import Flask
from endpoints import *
from flasgger import Swagger


def init_app() -> Flask:
    app = Flask("flights_monitor")
    app.register_blueprint(airport)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SWAGGER"] = {"openapi": "3.0.0"}
    swagger = Swagger(app, template_file="docs/openapi.yaml")
    return app


if __name__ == "__main__":
    app = init_app()
    app.run()
