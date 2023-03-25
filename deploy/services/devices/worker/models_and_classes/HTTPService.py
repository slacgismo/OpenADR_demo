import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler


class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_error(404)


class HealthCheckService:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.path = path

    def run(self, long_process_fn, long_process_args):

        server_thread = threading.Thread(target=self.start_http_server)
        server_thread.start()

        if long_process_fn:
            long_process_thread = threading.Thread(
                target=long_process_fn, args=long_process_args)
            long_process_thread.start()
            long_process_thread.join()  # Wait for the thread to finish

    def start_http_server(self):
        server = HTTPServer((self.host, self.port), HealthCheckServer)
        print(f"Starting HTTP server on {self.host}:{self.port}")
        server.serve_forever()
