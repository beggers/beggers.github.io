"""
A basic webserver to test the site layout and pages.
"""

import logging
import os


def find_file(host: str, content_dir: str) -> tuple[bytes, str]:
    fragments = host.split(".")[:-1]
    fragments.reverse()
    logging.debug(f"Finding file for host {host} with fragments {fragments}")

    path = os.path.join(content_dir, "index.html")  # default
    if fragments:
        new_path = os.path.join(content_dir, *fragments[:-1])
        matching_files_at_path = [
            filename
            for filename in os.listdir(new_path)
            if filename.startswith(fragments[-1])
        ]
        assert (
            len(matching_files_at_path) == 0
            or len(matching_files_at_path) == 1
            or len(matching_files_at_path) == 2
        )
        for filename in matching_files_at_path:
            if os.path.isfile(os.path.join(new_path, filename)):
                new_path = os.path.join(new_path, filename)
                break
            elif os.path.isdir(os.path.join(new_path, filename)):
                new_path = os.path.join(new_path, filename)
        else:
            new_path = os.path.join(new_path, "index.html")
        path = new_path

    with open(path, "rb") as f:
        return f.read(), "html"
