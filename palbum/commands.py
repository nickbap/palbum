import click

from palbum.utils import download_images_from_dbx


@click.command()
def download_images():
    """Download new images from Dropbox"""
    download_images_from_dbx()
