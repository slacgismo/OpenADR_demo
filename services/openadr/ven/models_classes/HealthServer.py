

from aiohttp import web
import logging


class HealthServer:
    def __init__(self, host='localhost', port=None, path='/health'):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.add_routes([web.get(path, self.handle_health)])

    async def handle_health(self, request):
        return web.Response(text='ok')

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print("===================================")
        print(
            f'VEN Health Server at http://{self.host}:{self.port}/health')
        print("===================================")

    async def stop(self):
        await self.app.shutdown()
