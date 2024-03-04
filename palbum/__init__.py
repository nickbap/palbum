from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(config["config"])

    db.init_app(app)
    migrate.init_app(app, db)

    from palbum.routes import main

    app.register_blueprint(main)

    from palbum import models  # noqa: F401

    return app
