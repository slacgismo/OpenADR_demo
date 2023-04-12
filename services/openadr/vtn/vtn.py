import functools
import logging
import os
import asyncio
from datetime import datetime, timezone, timedelta
import pytz
from openleadr import OpenADRServer, enable_default_logging
from openleadr.utils import generate_id
from functools import partial
from aiohttp import web
from actions.handle_order import handle_order
from actions.handle_meter import handle_meter
from actions.handle_health_check import handle_health_check
from actions.handle_all_ven_info import handle_all_ven_info
from actions.handle_device import check_device_id_from_tess_device_api
from actions.handle_dispatch import handle_dispatch
from utils.guid import guid
from classes.SharedVenInfos import SharedVenInfos
from utils.parse_device_id_from_ven_id import parse_device_id_from_ven_id
logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)


try:
    ENV = os.environ['ENV']
    AGENT_ID = os.environ['AGENT_ID']
    RESOURCE_ID = os.environ['RESOURCE_ID']
    MARKET_INTERVAL_IN_SECONDS = os.environ['MARKET_INTERVAL_IN_SECONDS']
    METER_API_URL = os.environ['METER_API_URL']
    DEVICES_API_URL = os.environ['DEVICES_API_URL']
    ORDERS_API_URL = os.environ['ORDERS_API_URL']
    DISPATCHES_API_URL = os.environ['DISPATCHES_API_URL']
except Exception as e:
    raise Exception(f"ENV is not set correctly: {e}")
# tz_local = pytz.timezone(LOCAL_TIMEZONE)
VTN_ID = 'vtn-' + AGENT_ID
MARKET_START_TIME = "2020-01-01T00:00:00Z"


# Future db
VENS = {
    "ven-0": {
        "ven_name": "ven-0",
        "ven_id": "ven-0",
        "registration_id": "reg-id-0"
    }
}

shared_ven_info = SharedVenInfos.get_instance()
shared_ven_info.set_anget_id(AGENT_ID)
shared_ven_info.set_resource_id(RESOURCE_ID)
shared_ven_info.set_vtn_id(VTN_ID)
shared_ven_info.set_market_interval_in_seconds(MARKET_INTERVAL_IN_SECONDS)


async def on_create_party_registration(registration_info, DEVICES_API_URL: str):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    ven_id = registration_info['ven_name']
    ven_name = ven_id
    if ven_name in VENS:
        return ven_id, VENS[ven_name]['registration_id']

    else:
        logging.info("=======================================")
        logging.info(
            f"ven_name {ven_name} is not in VENS,add to VTN")
        logging.info("=======================================")
        device_id = ven_id
        registration_id = str(guid())
        VENS[ven_name] = {
            "device_id": device_id,
            "ven_name": ven_name,
            "registration_id": registration_id
        }
        return ven_id, registration_id
        # device_id = parse_device_id_from_ven_id(ven_id)

        # response = await check_device_id_from_tess_device_api(
        #     ven_id=ven_id,
        #     device_id=device_id,
        #     agent_id=None,
        #     resource_id=None,
        #     DEVICES_API_URL=DEVICES_API_URL
        # )

        # if response.status == 200:
        #     logging.info("======================================1=")
        #     registration_id = str(guid())
        # VENS[ven_name] = {
        #     "device_id": device_id,
        #     "ven_name": ven_name,
        #     "registration_id": registration_id
        # }
        #     logging.info(
        #         f"VEN {ven_name} registered with registration_id {registration_id}")
        #     return ven_id, registration_id

        # else:
        #     return False


async def ven_lookup(ven_id):
    if ven_id in VENS:
        return {'ven_id': ven_id,
                'ven_name': ven_id,
                'registration_id': VENS[ven_id]['registration_id']}
    else:
        logging.info("***************************************")
        logging.info(f"ven_lookup {ven_id} not found VENS {VENS}")
        logging.info("***************************************")
        return {}

if __name__ == "__main__":

    # Create the server object
    server = OpenADRServer(vtn_id='myvtn',
                           http_host='0.0.0.0',
                           ven_lookup=ven_lookup)

    # Add the handler for client (VEN) registrations
    server.add_handler('on_create_party_registration',
                       functools.partial(on_create_party_registration, DEVICES_API_URL=DEVICES_API_URL))

    # Add the handler for report registrations from the VEN
    # server.add_handler('on_register_report', on_register_report)

    server.app.add_routes([
        # web.get('/trigger/{minutes_duration}', handle_trigger_event),
        # web.get('/cancel', handle_cancel_event),
        web.put('/dispatch/{ven_id}', functools.partial(handle_dispatch,
                                                        DISPATCHES_API_URL=DISPATCHES_API_URL)),
        web.put('/order/{ven_id}', functools.partial(handle_order,
                ORDERS_API_URL=ORDERS_API_URL)),
        web.put('/meter/{ven_id}', functools.partial(handle_meter,
                                                     METER_API_URL=METER_API_URL, MARKET_INTERVAL_IN_SECONDS=int(MARKET_INTERVAL_IN_SECONDS))),
        # web.get('/vens', functools.partial(handle_all_ven_info, VENS=VENS)),
        web.get('/health', handle_health_check)
    ])

    # logging.debug(f"Configured server {server}")

    loop = asyncio.new_event_loop()
    # loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.create_task(server.run())
    loop.run_forever()
