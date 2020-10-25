import os

from pydoc import locate

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .api.routes import routes

db_sql_alchemy = SQLAlchemy()
cors = CORS()


def _initialize_routes(api):
    for route in routes:
        klass, resource_routes = route
        api.add_resource(locate(klass), *resource_routes)


def create_app(app_settings=None):
    app = Flask(__name__)

    if app_settings is None:
        app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db_sql_alchemy.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    api = Api(app)
    _initialize_routes(api)

    # shell context for flask cli
    @app.shell_context_processor
    def make_shell_context():
        return {"app": app, "db": db_sql_alchemy}

    return app
