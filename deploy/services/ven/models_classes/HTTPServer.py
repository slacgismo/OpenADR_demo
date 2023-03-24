import aiohttp
import asyncio
import logging
import time


class HTTPServer:
    def __init__(self):
        self.app = aiohttp.web.Application()
        self.app.add_routes(
            [aiohttp.web.get('/healthcheck', self.handle_healthcheck)])
        self.runner = aiohttp.web.AppRunner(self.app)

    async def start(self):
        await self.runner.setup()
        site = aiohttp.web.TCPSite(self.runner, '0.0.0.0', 8000)
        await site.start()

    async def stop(self):
        await self.runner.cleanup()

    async def handle_healthcheck(self, request):
        return aiohttp.web.Response(text="OK")

    async def check_thirdparty_api(self):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://google.com') as response:
                        response_text = await response.text()
                        logging.info(
                            f"Third-party API response: {response_text}")
            except Exception as e:
                logging.error(f"Error checking third-party API: {e}")
            await asyncio.sleep(10)
