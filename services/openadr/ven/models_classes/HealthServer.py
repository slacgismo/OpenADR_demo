

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import asyncio
import time
import logging
import time
from helper.conver_date_to_timestamp import wait_till_next_market_start_time, current_market_start_timestamp
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
from api.sonnen_battery.filter_battery_data import filter_battery_data
from .Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS

from aiohttp import web
import logging


class HealthServer:
    def __init__(self, host='localhost', port=8888, path='/health'):
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


# async def async_task():
#     while True:
#         print('Async task running')
#         await asyncio.sleep(1)

# class HttpServer:
#     def __init__(self, host: str, port: int, path: str):
#         self.host = host
#         self.port = port
#         self.path = path

#     async def health_check(self, request):
#         return web.Response(text='Okay')

#     async def run_server(self):
#         app = web.Application()
#         app.router.add_get(self.path, self.health_check)

#         runner = web.AppRunner(app)
#         await runner.setup()

#         site = web.TCPSite(runner, self.host, self.port)
#         await site.start()

#         # Wait for the server to shut down
#         await asyncio.Event().wait()

# async def health_handler(request):
#     print("Health check")
#     return web.Response(text="OK")


# class HttpServer:
#     def __init__(self, host="localhost", port=8000, path="/health"):
#         self.host = host
#         self.port = port
#         self.app = web.Application()
#         self.path = path
#         self.app.add_routes([web.get(self.path, health_handler)])
#         self.runner = web.AppRunner(self.app)

#     async def start(self):
#         logging.info("===================================")
#         logging.info(
#             f"Starting HTTP server: {self.host}:{self.port}/{self.path}")
#         logging.info("===================================")
#         await self.runner.setup()
#         site = web.TCPSite(self.runner, self.host, self.port)
#         await site.start()

#     async def stop(self):
#         await self.runner.cleanup()


# import aiohttp
# import asyncio
# import logging
# import time
# from helper.conver_date_to_timestamp import wait_till_next_market_start_time, current_market_start_timestamp
# from api.sonnen_battery.sonnen_api import SonnenInterface
# from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
# from api.sonnen_battery.filter_battery_data import filter_battery_data
# from .Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
# from .get_devices_data import get_devices_data


# class HTTPServer:
#     def __init__(self, healthcheck_port: int = 8000, ven_id: str = "ven123"):
#         self.app = aiohttp.web.Application()
#         self.healthcheck_port = healthcheck_port
#         self.ven_id = ven_id
#         self.app.add_routes(
#             [aiohttp.web.get('/health', self.handle_healthcheck)])
#         self.runner = aiohttp.web.AppRunner(self.app)

#     async def start(self):
#         await self.runner.setup()
#         site = aiohttp.web.TCPSite(
#             self.runner, '0.0.0.0', self.healthcheck_port)
#         await site.start()

#     async def stop(self):
#         await self.runner.cleanup()

#     async def handle_healthcheck(self, request):
#         return aiohttp.web.Response(text=f"ven: {self.ven_id} OK")

#     async def submit_order_to_vtn(self,
#                                   vtn_order_url: str = None,
#                                   market_interval: int = 60,
#                                   market_start_time: str = None,
#                                   queue: asyncio.Queue = None,
#                                   advanced_seconds: int = 0,
#                                   lock: asyncio.Lock = None
#                                   ):
#         logging.info("Submit order at market start time")
#         while True:
#             await wait_till_next_market_start_time(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval,
#                 # one second before market start time
#                 advanced_seconds=advanced_seconds,
#                 funciton_name="submit_order_to_vtn"

#             )
#             makret_start_time = current_market_start_timestamp(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval
#             )
#             time_diff = int(time.time()) - makret_start_time
#             logging.info("------------------ order ------------------")
#             logging.info(
#                 f"start to submit order data at {time_diff} second after market start time: {makret_start_time}")
#             logging.info("------------------------------------")
#             try:

#                 device_data = await queue.get()
#                 if device_data is None:
#                     logging.info("====================================")
#                     logging.info("No device data to submit measurement")
#                     logging.info("====================================")
#                     return
#                 else:
#                     await self._put_data_to_order_api(
#                         device_data=device_data,
#                         vtn_order_url=vtn_order_url
#                     )

#             except Exception as e:
#                 raise Exception(f"Error get device data: {e}")

#     async def get_device_data(self,
#                               market_interval: int = 60,
#                               market_start_time: str = None,
#                               is_using_mock_device: bool = False,
#                               device_type: str = None,
#                               emulated_device_api_url: str = None,
#                               device_settings: dict = None,
#                               queue: asyncio.Queue = None,
#                               advanced_seconds: int = 0,
#                               lock: asyncio.Lock = None
#                               ):
#         logging.info(f"Get device before {advanced_seconds} market start time")
#         while True:
#             await wait_till_next_market_start_time(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval,
#                 advanced_seconds=advanced_seconds,
#                 funciton_name="get_device_data"
#             )
#             makret_start_time = current_market_start_timestamp(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval
#             )
#             time_diff = makret_start_time - int(time.time())
#             logging.info(
#                 "-------------- get device data ----------------------")
#             logging.info(
#                 f"start to get device data at {time_diff} second before market start time: {makret_start_time}")
#             logging.info("------------------------------------")
#             try:
#                 device_data = await get_devices_data(
#                     is_using_mock_device=is_using_mock_device,
#                     device_type=device_type,
#                     emulated_device_api_url=emulated_device_api_url,
#                     device_settings=device_settings
#                 )

#                 while not queue.empty():
#                     queue.get_nowait()
#                     logging.info("queue is not empty, clear queue")
#                     await asyncio.sleep(0.1)

#                 await queue.put(device_data)

#             except Exception as e:
#                 raise Exception(f"Error get device data: {e}")

#     async def submit_measurements_to_vtn(self,
#                                          vtn_measurement_url: str = None,
#                                          market_interval: int = 60,
#                                          market_start_time: str = None,
#                                          queue: asyncio.Queue = None,
#                                          advanced_seconds: int = 0,
#                                          lock: asyncio.Lock = None
#                                          ):

#         if market_interval is None or market_start_time is None:
#             raise Exception(
#                 "market_interval, device_type, market_start_time cannot be None")
#         while True:

#             await wait_till_next_market_start_time(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval,
#                 advanced_seconds=advanced_seconds,
#                 funciton_name="submit_measurements_to_vtn"
#             )
#             logging.info("Submit measurement at market end time")
#             makret_start_time = current_market_start_timestamp(
#                 market_start_time=market_start_time,
#                 market_interval=market_interval
#             )
#             time_diff = int(time.time()) - makret_start_time
#             logging.info(
#                 "---------------submit device data ---------------------")
#             logging.info(
#                 f"start to submit device data at {time_diff} second after market start time: {makret_start_time}")
#             logging.info("------------------------------------")
#             try:

#                 device_data = await queue.get()
#                 if device_data is None:
#                     logging.info("====================================")
#                     logging.info("No device data to submit measurement")
#                     logging.info("====================================")
#                     return
#                 else:
#                     await self._put_data_to_meter_api(
#                         data=device_data,
#                         vtn_measurement_url=vtn_measurement_url
#                     )

#             except Exception as e:
#                 raise Exception(f"Error get device data: {e}")

#     async def _put_data_to_meter_api(
#         self,
#         data: dict = None,
#         vtn_measurement_url: str = None,
#     ):
#         if data is None or vtn_measurement_url is None:
#             raise Exception(
#                 "data, vtn_measurement_endpoint cannot be None")

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.put(vtn_measurement_url, json=data) as response:
#                     response_text = await response.text()
#                     if response.status != 200:
#                         # TODO: handle 400, 401, 403, 404, 500
#                         raise Exception(
#                             f"Submit measurements to Meter API response status code: {response.status}")
#                     else:
#                         logging.info("Send to Meter API success")

#         except Exception as e:
#             raise Exception(f"Error checking Meter API: {e}")
#         return response_text

#     async def _put_data_to_order_api(
#         self,
#         device_data: dict = None,
#         vtn_order_url: str = None,
#     ):
#         if device_data is None or vtn_order_url is None:
#             raise Exception(
#                 "data, vtn_measurement_endpoint cannot be None")

#         try:
#             async with aiohttp.ClientSession() as session:
#                 async with session.put(vtn_order_url, json=device_data) as response:
#                     response_text = await response.text()
#                     logging.info(
#                         f"Submit measurements to Meter API response: {response_text}")
#                     if response.status != 200:
#                         # TODO: handle 400, 401, 403, 404, 500
#                         raise Exception(
#                             f"Submit measurements to Meter API response status code: {response.status}")

#         except Exception as e:
#             raise Exception(f"Error checking Meter API: {e}")
#         return response_text
