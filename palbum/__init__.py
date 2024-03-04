from flask import Flask

from config import config


def create_app():
    app = Flask(__name__)

    app.config.from_object(config["config"])

    from palbum.routes import main

    app.register_blueprint(main)
    return app
