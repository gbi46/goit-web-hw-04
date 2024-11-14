from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import mimetypes
import pathlib
import socket
import urllib.parse

class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.parent_path = pathlib.Path(__file__).parent
        super().__init__(request, client_address, server)

    def send_to_socket_server(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            data = json.dumps(data)
            sock.sendto(data.encode(), ('localhost', 5000))

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
         
        if pr_url.path == '/':
            self.send_html_file(self.parent_path / 'index.html')
        elif pr_url.path == '/message':
            self.send_html_file(self.parent_path / 'message.html')
        else:
            if self.parent_path.joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
               self.send_html_file(self.parent_path / 'error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length).decode()

        parse_data = { 
            key: urllib.parse.unquote_plus(val) for key, val in [ el.split("=") for el in data.split("&")]
        }

        timestamp = str(datetime.now())
        data_record = {
            timestamp: parse_data
        }

        self.send_to_socket_server(data_record)

        response_content = f"""
            <p>Success</p><br />
            <a href='/message.html'>Message page</a><br />
            <a href='/'>Main page</a>
        """

        self.send_response(200)
        self.send_header("Content-Type", 'text/html')
        self.end_headers()
        self.wfile.write(response_content.encode())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)

        full_path = pathlib.Path(__file__).parent / self.path.lstrip('/')

        mt = mimetypes.guess_type(full_path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        
        with open(full_path, 'rb') as file:
            self.wfile.write(file.read())