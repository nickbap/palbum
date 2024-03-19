from datetime import datetime

from palbum import db
from palbum.constants import PhotoOrder


class DisplaySettings(db.Model):
    __tablename__ = "display_settings"
    id = db.Column(db.Integer, primary_key=True)
    photo_order = db.Column(
        db.String(24), nullable=False, default=PhotoOrder.SEQUENTIAL
    )
    display_time = db.Column(db.Integer, nullable=False, default=5)
    fade = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<DisplaySettings {self.photo_order} {self.display_time} {self.fade}>"


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text, unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Image {self.id} {self.name}>"


class ImageMeta(db.Model):
    __tablename__ = "image_meta"
    id = db.Column(db.Integer, primary_key=True)
    last_image_id_shown = db.Column(db.Integer)

    def __repr__(self):
        return f"<ImageMeta {self.id} {self.last_image_id_shown}>"
