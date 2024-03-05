import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DBX_APP_KEY = os.environ.get("DBX_APP_KEY")
    DBX_APP_SECRET = os.environ.get("DBX_APP_SECRET")
    DBX_OAUTH2_REFRESH_TOKEN = os.environ.get("DBX_OAUTH2_REFRESH_TOKEN")
    IMAGES_DIR = "images"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SECRET_KEY"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "palbum.db")


config = {
    "config": Config,
}
