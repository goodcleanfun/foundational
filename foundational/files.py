import os
import shutil
import subprocess

import fsspec

from foundational.sizes import COPY_BUFFER_SIZE


def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def copy_file(filename, dest, buffer_size=COPY_BUFFER_SIZE):
    dest_kwargs = {}
    if dest.endswith(".gz") and not filename.endswith(".gz"):
        dest_kwargs.update(compression="gzip")
    elif dest.endswith(".zip") and not filename.endswith(".zip"):
        dest_kwargs.update(compression="zip")

    with fsspec.open(dest, "wb", **dest_kwargs) as df:
        with fsspec.open(filename, "rb") as sf:
            shutil.copyfileobj(sf, df)
    return dest


def remove_file(filename):
    os.unlink(filename)


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)
