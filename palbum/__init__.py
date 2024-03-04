import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "SECRET_KEY"

    from palbum.routes import main

    app.register_blueprint(main)
    return app
