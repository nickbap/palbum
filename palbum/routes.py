import random

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from palbum.forms import DisplaySettingsForm
from palbum.utils import IMAGES
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
def images():
    image_id = random.choice(IMAGES)
    return render_template("components/image.html", image_id=image_id)
