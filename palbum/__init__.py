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

    from palbum import commands
    from palbum import models  # noqa: F401

    app.cli.add_command(commands.download_images)

    if app.debug:
        from palbum import model_storage  # noqa: F401

        @app.shell_context_processor
        def make_shell_context():
            return {
                "db": db,
                "DisplaySettings": models.DisplaySettings,
                "DisplaySettingsModelStorage": model_storage.DisplaySettingseModelStorage,
                "Image": models.Image,
                "ImageModelStorage": model_storage.ImageModelStorage,
                "ImageMetaModelStorage": model_storage.ImageMetaModelStorage,
            }

    return app
