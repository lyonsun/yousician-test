from flask import Flask

from config import app_config
from db import mongo
from songs import songs


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config/__init__.py')

    mongo.init_app(app)

    app.register_blueprint(songs)

    return app
