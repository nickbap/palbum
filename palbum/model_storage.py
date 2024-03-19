from sqlalchemy.sql.expression import asc
from sqlalchemy.sql.expression import func

from palbum import db
from palbum.constants import PhotoOrder
from palbum.models import DisplaySettings
from palbum.models import Image
from palbum.models import ImageMeta


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


# TODO: test, update usage, remove utils.DisplaySettings
class DisplaySettingseModelStorage(BaseModelStorage):
    model = DisplaySettings

    @classmethod
    def create(cls):
        display_settings = cls.model()
        db.session.add(display_settings)
        db.session.commit()
        return display_settings

    @classmethod
    def read(cls):
        display_settings = cls.get_first()
        if display_settings:
            return display_settings
        return cls.create()

    @classmethod
    def update(cls, **kwargs):
        display_settings = cls.get_first()
        if not display_settings:
            display_settings = cls.create()

        for key, value in kwargs.items():
            if key in cls.model.__table__.columns.keys() and key not in {"id"}:
                setattr(display_settings, key, value)
        db.session.commit()


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
    def get_all_images_by_added_at(cls):
        return cls.model.query.order_by(asc("added_at")).all()

    @classmethod
    def get_random_image(cls):
        image_meta = ImageMetaModelStorage.get_last_image_id_shown()
        image = (
            cls.model.query.filter_by(is_visible=True)
            .filter(cls.model.id != image_meta.last_image_id_shown)
            .order_by(func.random())
            .limit(1)
            .first()
        )
        ImageMetaModelStorage.set_last_image_id_shown(image.id)
        return image

    @classmethod
    def get_sequential_image(cls):
        image_meta = ImageMetaModelStorage.get_last_image_id_shown()
        image = (
            cls.model.query.filter(
                cls.model.is_visible == True,  # noqa: E712
                cls.model.id > image_meta.last_image_id_shown,
            )
            .order_by(asc(cls.model.id))
            .limit(1)
            .first()
        )
        if not image:
            image = cls.model.query.filter_by(is_visible=True).first()
        ImageMetaModelStorage.set_last_image_id_shown(image.id)
        return image

    @classmethod
    def get_image_to_display(cls):
        display_settings = DisplaySettingseModelStorage.read()
        if display_settings.photo_order == PhotoOrder.RANDOM:
            return cls.get_random_image()
        elif display_settings.photo_order == PhotoOrder.SEQUENTIAL:
            return cls.get_sequential_image()
        else:
            return

    @classmethod
    def toggle_visibility(cls, image_id):
        image = cls.model.query.filter_by(id=image_id).first()
        if not image:
            return
        image.is_visible = not image.is_visible
        db.session.add(image)
        db.session.commit()
        return image


class ImageMetaModelStorage(BaseModelStorage):
    model = ImageMeta

    @classmethod
    def create(cls, image_id):
        image_meta = cls.model(last_image_id_shown=image_id)
        db.session.add(image_meta)
        db.session.commit()

    @classmethod
    def get_last_image_id_shown(cls):
        return cls.get_first()

    @classmethod
    def set_last_image_id_shown(cls, image_id):
        image_meta = cls.get_first()
        image_meta.last_image_id_shown = image_id
        db.session.commit()
