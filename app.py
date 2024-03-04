import json
import os
import random
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum

from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange

IMAGES = [
    "paso_01.JPG",
    "paso_02.JPG",
    "paso_03.JPG",
    "paso_04.JPG",
    "paso_05.JPG",
    "paso_06.JPG",
    "paso_07.JPG",
]


class PhotoOrder(str, Enum):
    RANDOM = "random"

    @classmethod
    def get_form_choices(cls):
        return [
            (value.value, key.title()) for key, value in PhotoOrder.__members__.items()
        ]


@dataclass
class DisplaySettings:
    json_name = "display_settings.json"

    photo_order: str
    display_time: int
    fade: bool

    def to_dict(self):
        return asdict(self)

    def save(self):
        with open(self.json_name, "w") as outfile:
            json.dump(self.to_dict(), outfile)

    @classmethod
    def read(cls):
        with open(cls.json_name, "r") as read_file:
            data = json.load(read_file)
            return cls(**data)


class DisplaySettingsForm(FlaskForm):
    photo_order = SelectField(
        "Photo Order",
        choices=PhotoOrder.get_form_choices(),
        validators=[DataRequired()],
    )
    display_time = IntegerField(
        "Photo Display Time (seconds)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=61, message="Display time must be 0 and 60"),
        ],
    )
    fade = BooleanField("Fade Out Transition")
    submit = SubmitField("Submit")


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "SECRET_KEY"


@app.route("/", methods=["GET", "POST"])
def home():
    settings = DisplaySettings.read()
    form = DisplaySettingsForm()

    if form.validate_on_submit():
        new_settings = DisplaySettings(
            form.photo_order.data, form.display_time.data, form.fade.data
        )
        new_settings.save()
        return redirect(url_for("home"))

    form.photo_order.data = settings.photo_order
    form.display_time.data = settings.display_time
    form.fade.data = settings.fade
    return render_template("index.html", form=form, settings=settings)


@app.route("/image")
def images():
    image_id = random.choice(IMAGES)
    return render_template("components/image.html", image_id=image_id)
