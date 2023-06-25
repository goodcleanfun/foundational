import os
import shutil

import fsspec
import furl
import requests

from foundational.files import ensure_dir


def save_response_content(response, destination):
    with fsspec.open(destination, "wb") as f:
        shutil.copyfileobj(response.raw, f)


def download_file(url, dest, retries=3, retry_delay=5, session=requests, headers=None):
    url = furl.furl(url)

    exists = os.path.exists(dest)
    is_dir = os.path.isdir(dest) if exists else len(os.path.splitext(dest)[1]) > 0

    base_dir = dest if is_dir else os.path.dirname(dest)
    ensure_dir(base_dir)

    dest_filename = os.path.basename(dest) if not is_dir else None
    if not dest_filename and url.path.isfile:
        dest_filename = url.path.segments[-1]
        dest = os.path.join(dest, dest_filename)

    with session.get(url, headers=headers, stream=True) as resp:
        resp.raw.decode_content = True
        resp.raise_for_status()
        save_response_content(resp, dest)

    return dest
