# import http.server
# import socketserver
# from aiohttp import web

from aiohttp import web
import aiohttp
import asyncio


class HTTPServer:
    def __init__(self, host: str = "127.0.0.1", port: int = "8070"):
        self.host = host
        self.port = port

    async def health_handler(self, request):
        return aiohttp.web.json_response({
            "statusCode": 200,
            "body": "OK"
        }
        )

    async def start(self):
        app = aiohttp.web.Application()
        app.router.add_get('/health', self.health_handler)
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, self.host, self.port)
        await site.start()

        while True:
            print("server is running")
            await asyncio.sleep(2)
