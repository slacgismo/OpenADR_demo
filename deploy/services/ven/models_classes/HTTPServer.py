import aiohttp
import asyncio
import logging
import time


class HTTPServer:
    def __init__(self, healthcheck_port: int = 8000, ven_id: str = "ven123"):
        self.app = aiohttp.web.Application()
        self.healthcheck_port = healthcheck_port
        self.ven_id = ven_id
        self.app.add_routes(
            [aiohttp.web.get('/healthcheck', self.handle_healthcheck)])
        self.runner = aiohttp.web.AppRunner(self.app)

    async def start(self):
        await self.runner.setup()
        site = aiohttp.web.TCPSite(
            self.runner, '0.0.0.0', self.healthcheck_port)
        await site.start()

    async def stop(self):
        await self.runner.cleanup()

    async def handle_healthcheck(self, request):
        return aiohttp.web.Response(text=f"ven: {self.ven_id} OK")

    async def check_thirdparty_api(self, thirdparty_api_url: str = "https://google.com", interval: int = 60):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(thirdparty_api_url) as response:
                        response_text = await response.text()
                        logging.info(
                            f"Third-party API response: {response_text}")
            except Exception as e:
                logging.error(f"Error checking third-party API: {e}")
            await asyncio.sleep(interval)
