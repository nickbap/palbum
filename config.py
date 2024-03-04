import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SECRET_KEY"


config = {
    "config": Config,
}
