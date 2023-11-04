"""
A basic webserver to test the site layout and pages.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

import mime_types

hostName = "localhost"
serverPort = 8080


CONTENT_DIR = "public"


def find_file(host):
    fragments = host.split(".")[:-1]
    fragments.reverse()

    # Build the path up to either the file or the directory.
    path = CONTENT_DIR
    for fragment in fragments[:-1]:
        path = os.path.join(path, fragment)

    # If it's a directory, look for index.html.
    if os.path.isdir(os.path.join(path, fragments[-1] if fragments else "")):
        path = os.path.join(path, "index.html")
        with open(path, "rb") as f:
            return f.read(), "html"

    # Not a directory -- grab the file.
    files = [f for f in os.listdir(path) if f.startswith(fragments[-1])]
    if len(files) != 1:
        raise ValueError(f"Multiple or no files found for {host}: {files}")
    file = files[0]
    path = os.path.join(path, file)

    with open(path, "rb") as f:
        return f.read(), file.split(".")[-1]


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers["Host"]
        resp, ext = find_file(host)
        self.send_response(200)
        self.send_header("Content-type", mime_types.extensions_to_types[ext])
        self.end_headers()
        self.wfile.write(resp)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
