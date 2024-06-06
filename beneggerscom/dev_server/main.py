from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import beneggerscom.utils.mime_types as mime_types

from beneggerscom.dev_server import find_file
from beneggerscom.utils.config import CONFIG


import logging


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
