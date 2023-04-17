import aiohttp
import asyncio
from datetime import timedelta
from aiohttp import web
import pytz
from openleadr import OpenADRClient, enable_default_logging
import os
import logging
import json
import threading
from models_classes.SharedDeviceInfo import SharedDeviceInfo
from actions.handle_get_device_data import handle_get_device_data
from models_classes.SharedDeviceData import SharedDeviceData
from models_classes.HealthServer import HealthServer
from helper.conver_date_to_timestamp import current_market_start_timestamp
from actions.handle_submit_order import submit_order_to_vtn
from actions.handle_event import handle_event
from actions.handle_dispatch import handle_dispatch
import functools
from actions.check_vtn import check_vtn_and_retry
from helper.str2bool import str2bool
try:
    ENVIRONMENT = os.environ['ENVIRONMENT']

    # Terraform
    EMULATED_DEVICE_API_URL = os.environ['EMULATED_DEVICE_API_URL']

    # from devices table
    DEVICE_TYPE = os.environ['DEVICE_TYPE']
    DEVICE_ID = os.environ['DEVICE_ID']

    # from agent table
    AGENT_ID = os.environ['AGENT_ID']
    RESOURCE_ID = os.environ['RESOURCE_ID']
    # from meters table
    METER_ID = os.environ['METER_ID']

    # from markets table
    MARKET_INTERVAL_IN_SECONDS = os.environ['MARKET_INTERVAL_IN_SECONDS']
    PRICE_FLOOR = os.environ['PRICE_FLOOR']
    PRICE_CEILING = os.environ['PRICE_CEILING']
    # from settings table
    DEVICE_SETTINGS = os.environ['DEVICE_SETTINGS']
except Exception as e:
    raise Exception(f"Environment variables is not set correctly: {e}")

# Constant that not change
VEN_HEALTH_CHECK_PORT = 8000
VEN_HEALTH_CHECK_SEVER = "0.0.0.0"
VEN_ID = DEVICE_ID
if ENVIRONMENT == "LOCAL":
    VTN_ADDRESS = 'vtn'
elif ENVIRONMENT == "AWS":
    # AWS ECS service always use the private ip 127.0.0.1
    VTN_ADDRESS = '127.0.0.1'
else:
    raise Exception(f"ENV:{ENVIRONMENT} is not set correctly")

VTN_PORT = '8080'
MARKET_START_TIME = "2020-01-01T00:00:00Z"
# VEN health check port
HTTPSERVER_PORT = "8000"


logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)

vtn_url = f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b"
logging.debug(f"VEN START {VEN_ID} {vtn_url} {RESOURCE_ID} {VEN_ID}")


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def main():

    try:

        vtn_base_url = f"http://{VTN_ADDRESS}:{VTN_PORT}"
        VTN_METER_URL = vtn_base_url + f"/meter/{VEN_ID}"
        VTN_ORDER_URL = vtn_base_url + f"/order/{VEN_ID}"
        VTN_DISPATCH_URL = vtn_base_url + f"/dispatch/{VEN_ID}"
        VTN_HEALTH_URL = vtn_base_url + f"/health"
        device_settings = json.loads(DEVICE_SETTINGS)
        is_using_mock_device_str = device_settings["is_using_mock_device"]
        is_using_mock_device = str2bool(is_using_mock_device_str)
        # check is using mock device type
        if is_using_mock_device:
            logging.info(f"Using mock device")
        else:
            logging.info(f"Using real device")

        flexible = device_settings["flexible"]
        # set shared global variables
        shared_device_info = SharedDeviceInfo.get_instance()
        shared_device_info.set_device_id(DEVICE_ID)
        shared_device_info.set_meter_id(METER_ID)
        shared_device_info.set_resource_id(RESOURCE_ID)
        shared_device_info.set_ven_id(VEN_ID)
        shared_device_info.set_agent_id(AGENT_ID)
        shared_device_info.set_flxible(int(flexible))
        shared_device_info.set_device_settings(device_settings)
        shared_device_info.set_device_type(DEVICE_TYPE)
        shared_device_info.set_emulated_device_api_url(EMULATED_DEVICE_API_URL)
        shared_device_info.set_is_using_mock_device(is_using_mock_device)
        market_interval = int(MARKET_INTERVAL_IN_SECONDS)
        shared_device_info.set_market_interval(market_interval)
        shared_device_info.set_market_start_time(MARKET_START_TIME)
        device_brand = device_settings["device_brand"]
        shared_device_info.set_price_ceiling(float(PRICE_CEILING))
        shared_device_info.set_price_floor(float(PRICE_FLOOR))

    except Exception as e:

        raise Exception(f"Envoronment variables is not set correctly: {e}")

    if check_vtn_and_retry(url=VTN_HEALTH_URL) is False:
        logging.error(f"VTN is not available: {vtn_url}")
        return

    client = OpenADRClient(
        ven_name=VEN_ID, vtn_url=f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b", debug=True)

    client.add_handler('on_event', functools.partial(
        handle_event, shared_device_info=shared_device_info))
    # Add event handling capability to the client

    loop1 = asyncio.new_event_loop()
    loop2 = asyncio.new_event_loop()
    loop3 = asyncio.new_event_loop()
    loop4 = asyncio.new_event_loop()
    # == == == == == == == == == start healthcheck server and openadr client in thread 1 == == == == == == == == ==
    # not work in container but work in local

    server = HealthServer(
        host=VEN_HEALTH_CHECK_SEVER, port=VEN_HEALTH_CHECK_PORT, path='/health')

    t1 = threading.Thread(target=start_loop, args=(loop1,))
    t1.start()
    asyncio.run_coroutine_threadsafe(client.run(), loop1)
    asyncio.run_coroutine_threadsafe(server.start(), loop1)

    # # ================== start the get device data thread 2 ==================
    t2 = threading.Thread(target=start_loop, args=(loop2,))
    t2.start()
    # run the get device data at end of market interval
    asyncio.run_coroutine_threadsafe(
        handle_get_device_data(
            device_brand=device_brand,
            device_id=DEVICE_ID,
            meter_id=METER_ID,
            resource_id=RESOURCE_ID,
            market_interval=int(MARKET_INTERVAL_IN_SECONDS),
            market_start_time=MARKET_START_TIME,
            is_using_mock_device=is_using_mock_device,
            device_type=DEVICE_TYPE,
            emulated_device_api_url=EMULATED_DEVICE_API_URL,
            device_settings=device_settings,
            advanced_seconds_of_market_startime=5,
            vtn_measurement_url=VTN_METER_URL,
        ), loop2)

    # ================== start the submit order thread 3 ==================
    # start of the market interval
    t3 = threading.Thread(target=start_loop, args=(loop3,))
    t3.start()
    asyncio.run_coroutine_threadsafe(
        submit_order_to_vtn(
            vtn_order_url=VTN_ORDER_URL,
            market_interval=int(MARKET_INTERVAL_IN_SECONDS),
            market_start_time=MARKET_START_TIME,
            advanced_seconds=0,
            price_ceiling=float(PRICE_CEILING),
            price_floor=float(PRICE_FLOOR)
        ), loop3
    )

    # ================== start the submit dispatch thread 4 ==================
    # end of market interval
    t4 = threading.Thread(target=start_loop, args=(loop4,))
    t4.start()
    asyncio.run_coroutine_threadsafe(
        handle_dispatch(
            vtn_dispatch_url=VTN_DISPATCH_URL,
            shared_device_info=shared_device_info,
        ), loop4
    )

    try:
        t1.join()
    finally:
        asyncio.run_coroutine_threadsafe(server.stop(), loop1)


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    main()
