from datetime import datetime

from palbum import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text, unique=True, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    @staticmethod
    def toggle_visibility(image_id):
        image = Image.query.filter_by(id=image_id).first()
        if not image:
            return
        image.is_visible = not image.is_visible
        db.session.add(image)
        db.session.commit()
        return image
