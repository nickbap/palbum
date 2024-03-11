from datetime import datetime

from palbum import db


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
