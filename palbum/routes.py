from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from sqlalchemy import asc

from palbum.forms import DisplaySettingsForm
from palbum.models import Image
from palbum.utils import DisplaySettings

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    form = DisplaySettingsForm()
    if form.validate_on_submit():
        new_settings = DisplaySettings(
            form.photo_order.data, form.display_time.data, form.fade.data
        )
        new_settings.save()
        return redirect(url_for("main.home"))

    settings = DisplaySettings.read()
    if settings:
        form.photo_order.data = settings.photo_order
        form.display_time.data = settings.display_time
        form.fade.data = settings.fade
    return render_template("index.html", form=form, settings=settings)


@main.route("/image")
def image():
    image = Image.get_random_image()
    return render_template("components/image.html", image=image)


@main.route("/images")
def images():
    images = Image.query.order_by(asc("added_at")).all()
    return render_template("images.html", images=images)


@main.route("/image/toggle/<int:image_id>", methods=["POST"])
def image_toggle(image_id):
    image = Image.toggle_visibility(image_id)
    return render_template("components/image-manager-image.html", image=image)
