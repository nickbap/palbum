from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange

from palbum.utils import PhotoOrder


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
