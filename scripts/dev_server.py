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

    # Build the path up to either the file or the directory.
    path = config["content_dir"]
    for fragment in fragments[:-1]:
        path = os.path.join(path, fragment)

    # If it's a directory, look for index.html.
    if os.path.isdir(os.path.join(path, fragments[-1] if fragments else "")):
        logging.info(f"Found directory matching host {host}: {path}")
        path = os.path.join(path, "index.html")
        with open(path, "rb") as f:
            return f.read(), "html"

    # Not a directory -- grab the file.
    files = [f for f in os.listdir(path) if f.startswith(fragments[-1])]
    if len(files) != 1:
        raise ValueError(f"Multiple or no files found for {host}: {files}")
    file = files[0]
    path = os.path.join(path, file)
    logging.info(f"Found file {file} matching {host} at {path}")

    with open(path, "rb") as f:
        return f.read(), file.split(".")[-1]


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
