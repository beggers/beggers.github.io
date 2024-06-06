"""
A basic webserver to test the site layout and pages.
"""

import json
import logging
import os

from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import mime_types


CONFIG = json.load(open("config.json"))


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


class Handler(SimpleHTTPRequestHandler):
    close_connection = True
    content_dir = CONFIG["content_dir"] if CONFIG else "."

    def do_GET(self):
        host = self.headers["Host"]

        resp, ext = find_file(host, self.content_dir)
        self.send_response(200)

        content_type = mime_types.extensions_to_types[ext]
        self.send_header("Content-type", content_type)

        self.end_headers()
        self.wfile.write(resp)


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=CONFIG.get("log_level", "INFO"))

    with ThreadingServer(
        (CONFIG["dev_hostname"], CONFIG["dev_port"]), Handler
    ) as server:
        server.content_dir = CONFIG["content_dir"]
        logging.info(
            "Server started http://%s:%s"
            % (CONFIG["dev_hostname"], CONFIG["dev_port"])
        )
        server.serve_forever()

    server.server_close()
    logging.info("Server stopped.")
