from sqlalchemy.sql.expression import func

from palbum import db
from palbum.models import Image


class BaseModelStorage:
    @classmethod
    def get(cls, id):
        return cls.model.query.get(id)

    @classmethod
    def get_first(cls):
        return cls.model.query.first()

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def filter_(cls, **kwargs):
        return cls.model.query.filter_by(**kwargs).all()

    @classmethod
    def get_by_id(cls, id):
        obj = cls.filter_(id=id)
        if not obj:
            return

        if len(obj) == 1:
            return obj[0]


class ImageModelStorage(BaseModelStorage):
    model = Image

    @classmethod
    def create(cls, name, is_visible=True):
        image = cls.model(name=name, is_visible=is_visible)
        db.session.add(image)
        db.session.commit()

    @classmethod
    def get_image_name_list(cls):
        return [image.name for image in cls.get_all()]

    @classmethod
    def get_random_image(cls):
        return (
            cls.model.query.filter_by(is_visible=True).order_by(func.random()).first()
        )

    @classmethod
    def toggle_visibility(cls, image_id):
        image = cls.model.query.filter_by(id=image_id).first()
        if not image:
            return
        image.is_visible = not image.is_visible
        db.session.add(image)
        db.session.commit()
        return image
