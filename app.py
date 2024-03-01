import json
import random

from dataclasses import asdict
from dataclasses import dataclass

from flask import Flask
from flask import render_template

IMAGES = [
    "paso_01.JPG",
    "paso_02.JPG",
    "paso_03.JPG",
    "paso_04.JPG",
    "paso_05.JPG",
    "paso_06.JPG",
    "paso_07.JPG",
]


@dataclass
class DisplaySettings:
    json_name = "display_settings.json"

    photo_order: str
    display_time: int

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


app = Flask(__name__)


@app.route("/")
def home():
    settings = DisplaySettings.read()
    return render_template("index.html", display_time=settings.display_time)


@app.route("/image")
def images():
    image_id = random.choice(IMAGES)
    return render_template("components/image.html", image_id=image_id)


if __name__ == "__main__":
    app.run(debug=True)
