import random
from datetime import datetime

from palbum import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text, unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    @staticmethod
    def get_image_name_list():
        return [image.name for image in Image.query.all()]

    @staticmethod
    def get_random_image():
        return random.choice(Image.get_image_name_list())

    @classmethod
    def create(cls, name, is_visible=True):
        image = cls(name=name, is_visible=is_visible)
        db.session.add(image)
        db.session.commit()
