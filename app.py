import random


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

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/image")
def images():
    image_id = random.choice(IMAGES)
    return render_template("components/image.html", image_id=image_id)


if __name__ == "__main__":
    app.run(debug=True)
