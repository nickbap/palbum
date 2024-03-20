import os
from threading import Thread

import dropbox
from flask import current_app
from PIL import Image as PILImage
from PIL import ImageOps

from palbum.model_storage import ImageModelStorage


def download_images_from_dbx_async():
    Thread(
        target=_download_images_from_dbx_async,
        args=(current_app._get_current_object(),),
    ).start()


def _download_images_from_dbx_async(app):
    with app.app_context():
        download_images_from_dbx()


def get_image_dir_path(file_name=None):
    if file_name:
        return os.path.join(
            current_app.static_folder, current_app.config["IMAGES_DIR"], file_name
        )
    return os.path.join(current_app.static_folder, current_app.config["IMAGES_DIR"])


def maybe_create_image_dir_path():
    image_dir_path = get_image_dir_path()
    if not os.path.exists(image_dir_path):
        os.makedirs(image_dir_path)


def download_images_from_dbx():
    dbx = dropbox.Dropbox(
        app_key=current_app.config["DBX_APP_KEY"],
        app_secret=current_app.config["DBX_APP_SECRET"],
        oauth2_refresh_token=current_app.config["DBX_OAUTH2_REFRESH_TOKEN"],
    )

    dbx_files = dbx.files_list_folder("/palbum")

    dbx_image_map = {
        entry.name: entry
        for entry in dbx_files.entries
        if dbx_files and dbx_files.entries
    }
    if not dbx_image_map:
        return

    current_image_list = ImageModelStorage.get_image_name_list()
    images_to_download = set(dbx_image_map.keys()).difference(set(current_image_list))
    if not images_to_download:
        print("No new images to download")
        return

    print(
        f"{len(images_to_download)} new image{'s'if len(images_to_download) > 1 else ''} need to be downloaded"
    )

    maybe_create_image_dir_path()
    for image in images_to_download:
        dbx_file = dbx_image_map.get(image)
        if not dbx_file:
            print(f"{image} not found!")
            continue
        try:
            print(f"Downloading: {image}")

            dbx.files_download_to_file(
                get_image_dir_path(dbx_file.name),
                dbx_file.path_lower,
            )

            _revise_image(image)

            ImageModelStorage.create(image)

            print(f"{image} downloaded and saved successfully")
        except Exception as e:
            print(f"{e} hit while processing {image}")
            continue


def _revise_image(image):
    image_path = get_image_dir_path(image)
    img = PILImage.open(image_path)

    revised_img = ImageOps.exif_transpose(img)

    img.close()

    if _is_bigger_than_1000px(revised_img):
        revised_img = _resize_image_to_1000px(revised_img)

    revised_img.save(image_path, optimize=True, quality="web_maximum")
    revised_img.close()


def _is_bigger_than_1000px(img):
    return img.width > 1000 or img.height > 1000


def _resize_image_to_1000px(img):
    big_attr = "height" if img.height >= img.width else "width"
    multiplier = 1000 / getattr(img, big_attr)
    return img.resize(
        (int(img.width * multiplier), int(img.height * multiplier)),
        PILImage.LANCZOS,
    )
