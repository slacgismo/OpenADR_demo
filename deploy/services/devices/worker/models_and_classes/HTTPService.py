import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import time


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK\n')


class HTTPService:
    def __init__(self, host, port, health_path):
        self.host = host
        self.port = port
        self.health_path = health_path

    def run(self):
        server = HTTPServer((self.host, self.port), HealthCheckHandler)
        print(f"Starting HTTP server on {self.host}:{self.port}")
        server.serve_forever()
