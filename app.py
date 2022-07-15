from flask import Flask
from endpoints import *
from flasgger import Swagger
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        print(items)
        self.regex = items[0]


def init_app() -> Flask:
    app = Flask("flights_monitor")
    app.url_map.converters['regex'] = RegexConverter
    app.register_blueprint(airport)
    app.register_blueprint(country)
    app.config["JSON_SORT_KEYS"] = False
    app.config["SWAGGER"] = {"openapi": "3.0.0"}
    swagger = Swagger(app, template_file="docs/openapi.yaml")
    return app


app = init_app()
app.run()
