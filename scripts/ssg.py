"""
A simple static site generator to make the site. MUST be run from the top-
level directory.

Errors if there are multiple definitions for the same output resource.
"""


import os
import shutil


LAYOUTS_DIR = "layouts"
OUTPUT_DIR = "public"
PAGES_DIR = "pages"
STATIC_DIR = "static"
STYLE_DIR = "styles"


def main():
    statics = _get_all_from_directory(STATIC_DIR)
    for static in statics:
        _copy_file_to_output(static)


def _get_all_from_directory(d):
    files = []
    for root, _, fs in os.walk(d):
        for f in fs:
            files.append(os.path.join(root, f))
    return files


def _copy_file_to_output(path):
    shutil.copy(path, path.replace(STATIC_DIR, OUTPUT_DIR))


if __name__ == "__main__":
    main()
