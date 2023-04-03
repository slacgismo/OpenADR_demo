# import asyncio
# import threading
# from http.server import HTTPServer, BaseHTTPRequestHandler


# class LongProcess:
#     def __init__(self):
#         self._message = None
#         self._lock = threading.Lock()

#     async def run(self):
#         while True:
#             with self._lock:
#                 self._message = self._generate_message()
#             await asyncio.sleep(1)

#     def _generate_message(self):
#         # Replace this with your own message generation logic
#         return "Hello, world!"

#     def get_message(self):
#         with self._lock:
#             return self._message


# class HTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/health":
#             self.send_response(200)
#             self.send_header("Content-type", "text/plain")
#             self.end_headers()
#             self.wfile.write(b"OK")
#         else:
#             self.send_error(404)


# class HTTPServerThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self._server = HTTPServer(("localhost", 8000), HTTPRequestHandler)

#     def run(self):
#         self._server.serve_forever()


# if __name__ == "__main__":
#     # Start the HTTP server in a separate thread
#     server_thread = HTTPServerThread()
#     server_thread.start()

#     # Start the long process in the main thread
#     long_process = LongProcess()
#     asyncio.run(long_process.run())

#     # Wait for the HTTP server thread to finish
#     server_thread.join()

import asyncio
import logging
from aiohttp import web

from http import HTTPStatus
from typing import Dict
import json


def simulate_http_response(data: Dict) -> Dict:
    response = {
        'statusCode': HTTPStatus.OK,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': data
    }
    return web.json_response(response, status=200)


response_data = {"message": "Hello, world!"}
response = simulate_http_response(response_data)

json_data = json.loads(response.text)
print("json_data: ", json_data['body'])

# data = json.loads(body_data)
# message = data["message"]
