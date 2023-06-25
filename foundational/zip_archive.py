import os
import zipfile

import fsspec

from foundational.iterables import iterify


def unzip_all_files(zip_filename, out_dir=None, full_path=True):
    if out_dir is None:
        out_dir = os.path.dirname(zip_filename) or os.curdir

    if os.path.isdir(out_dir) and not out_dir.endswith(os.sep):
        out_dir += os.sep

    paths = []

    with fsspec.open(zip_filename).open() as f:
        zf = zipfile.ZipFile(f)

        for path in zf.infolist():
            filename = path.filename
            base_filename = os.path.basename(filename)
            extract_path = filename if full_path else base_filename
            out_filename = os.path.join(out_dir, extract_path)
            zf.extract(extract_path, out_dir)
            paths.append(out_filename)
    return paths


def extract_filenames_from_zip(zip_filename, filenames, out_dir, full_path=True):
    filenames = iterify(filenames)

    if os.path.isdir(out_dir) and not out_dir.endswith(os.sep):
        out_dir += os.sep

    with fsspec.open(zip_filename).open() as f:
        zf = zipfile.ZipFile(f)

        paths = []

        for path in zf.infolist():
            filename = path.filename
            base_filename = os.path.basename(filename)
            if filename in filenames or base_filename in filenames:
                extract_path = filename if full_path else base_filename
                out_filename = os.path.join(out_dir, extract_path)
                zf.extract(extract_path, out_dir)
                paths.append(out_filename)

    if len(filenames) > 1:
        return paths
    elif len(filenames) > 0:
        return paths[0]
    else:
        return None
