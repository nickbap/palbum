from palbum import create_app
from palbum import db
from palbum.models import Image

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Image": Image}
