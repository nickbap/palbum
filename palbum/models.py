import random
from datetime import datetime

from palbum import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text, unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def create(cls, name, is_visible=True):
        image = cls(name=name, is_visible=is_visible)
        db.session.add(image)
        db.session.commit()

    @staticmethod
    def get_image_name_list():
        return [image.name for image in Image.query.all()]

    @staticmethod
    def get_random_image():
        images = Image.query.filter_by(is_visible=True).all()
        return random.choice(images)

    @staticmethod
    def toggle_visibility(image_id):
        image = Image.query.filter_by(id=image_id).first()
        if not image:
            return
        image.is_visible = not image.is_visible
        db.session.add(image)
        db.session.commit()
        return image
