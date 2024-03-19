from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for

from palbum.forms import DisplaySettingsForm
from palbum.model_storage import DisplaySettingseModelStorage
from palbum.model_storage import ImageModelStorage

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():
    form = DisplaySettingsForm()
    if form.validate_on_submit():
        DisplaySettingseModelStorage.update(
            photo_order=form.photo_order.data,
            display_time=form.display_time.data,
            fade=form.fade.data,
        )
        return redirect(url_for("main.home"))

    settings = DisplaySettingseModelStorage.read()
    if settings:
        form.photo_order.data = settings.photo_order
        form.display_time.data = settings.display_time
        form.fade.data = settings.fade
    return render_template("index.html", form=form, settings=settings)


@main.route("/image")
def image():
    image = ImageModelStorage.get_image_to_display()
    return render_template("components/image.html", image=image)


@main.route("/images")
def images():
    images = ImageModelStorage.get_all_images_by_added_at()
    return render_template("images.html", images=images)


@main.route("/image/toggle/<int:image_id>", methods=["POST"])
def image_toggle(image_id):
    image = ImageModelStorage.toggle_visibility(image_id)
    return render_template("components/image-manager-image.html", image=image)
