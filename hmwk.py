from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
import os
import cgi
import pandas as pd

PAGE = """\
<html>
<body>
<p>Hello, web!</p>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests by returning a fixed "page"."""

    def _set_headers(self, content):
        self.send_response(200)
        # can specify another header to specify encoding
        # legacy code from websites of another language
        self.send_header('Content-type', 'text/html')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()

    # Handle a GET request.
    def do_GET(self):
        filepath = urlparse(self.path).path
        if filepath.startswith(sep):
            filepath = filepath[1:]
        try:
            f = open(filepath, 'r')
            content = bytes(f.read(), "utf-8")
            self._set_headers(content)
            self.wfile.write(content)
            f.close()
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def incorporate_content(self, data):
        page = BeautifulSoup(PAGE, "html.parser")
        data = BeautifulSoup(data, "html.parser")
        return page.body.append(data)

    # Handle a POST request
    # Inspired by:
    # https://stackoverflow.com/questions/28217869/python-basehttpserver-file-upload-with-maxfile-size
    def do_POST(self):
        # Writing a copy of the content to file
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                    })
        filename = form['file'].filename
        data = form['file'].file.read()
        open("/tmp/%s"%filename, "wb").write(data)
        content = pd.read_csv("/tmp/%s"%filename).to_html()
        # Creating content
        # content = self.incorporate_content(content)
        content = bytes(content, "utf-8")
        self._set_headers(content)
        self.wfile.write(content)

if __name__ == "__main__":
    server_address = ("", 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
