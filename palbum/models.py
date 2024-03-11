from datetime import datetime

from palbum import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text, unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
