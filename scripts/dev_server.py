"""
A basic webserver to test the site layout and pages.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os

import mime_types


config = json.load(open("config.json"))


def find_file(host):
    fragments = host.split(".")[:-1]
    fragments.reverse()
    logging.debug(f"Finding file for host {host} with fragments {fragments}")

    # Build the path up to either the file or the directory.
    path = config["content_dir"]
    for fragment in fragments[:-1]:
        path = os.path.join(path, fragment)
    logging.debug(f"Search path for host {host}: {path}")

    # Check for a matching file.
    files = [
        f
        for f in os.listdir(path)
        if f.startswith(fragments[-1]) and f.endswith(".html")
    ]
    print(files)
    if len(files) == 1:
        file = files[0]
        path = os.path.join(path, file)
        logging.info(f"Found file {file} matching {host} at {path}")
    elif os.path.isdir(os.path.join(path, fragments[-1] if fragments else "")):
        path = os.path.join(path, fragments[-1] if fragments else "")
        logging.info(f"Found directory matching host {host}: {path}")
        path = os.path.join(path, "index.html")
    else:
        logging.error(f"No file or directory matching host {host}")
        return b"404 Not Found", "html"

    with open(path, "rb") as f:
        return f.read(), "html"

    # Not a directory -- grab the file.


class DevBenEggersComServer(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers["Host"]
        logging.info(f"GET {host}")

        resp, ext = find_file(host)
        self.send_response(200)

        content_type = mime_types.extensions_to_types[ext]
        logging.info(f"Content-Type: {content_type}")
        self.send_header("Content-type", content_type)

        self.end_headers()
        self.wfile.write(resp)


if __name__ == "__main__":
    logging.basicConfig(level=config.get("log_level", "INFO"))

    server = HTTPServer(
        (config["dev_hostname"], config["dev_port"]), DevBenEggersComServer
    )
    server.content_dir = config["content_dir"]
    logging.info(
        "Server started http://%s:%s" % (config["dev_hostname"], config["dev_port"])
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    logging.info("Server stopped.")
