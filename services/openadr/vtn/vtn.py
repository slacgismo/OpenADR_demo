import functools
import logging
import os
import asyncio

from openleadr import OpenADRServer

from aiohttp import web
from actions.handle_order import handle_order
from actions.handle_meter import handle_meter
from actions.handle_health_check import handle_health_check
# from actions.handle_device import check_device_id_from_tess_device_api
from actions.handle_dispatch import handle_dispatch
from utils.guid import guid
from classes.SharedVenInfos import SharedVenInfos
logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)


try:
    ENVIRONMENT = os.environ['ENVIRONMENT']
    AGENT_ID = os.environ['AGENT_ID']
    RESOURCE_ID = os.environ['RESOURCE_ID']
    MARKET_INTERVAL_IN_SECONDS = os.environ['MARKET_INTERVAL_IN_SECONDS']
    METERS_API_URL = os.environ['METERS_API_URL']
    DEVICES_API_URL = os.environ['DEVICES_API_URL']
    ORDERS_API_URL = os.environ['ORDERS_API_URL']
    DISPATCHES_API_URL = os.environ['DISPATCHES_API_URL']
except Exception as e:
    raise Exception(f"environment variables is not set correctly: {e}")
# tz_local = pytz.timezone(LOCAL_TIMEZONE)
VTN_ID = 'vtn-' + AGENT_ID
MARKET_START_TIME = "2020-01-01T00:00:00Z"


# openadr
VENS = {}


shared_ven_info = SharedVenInfos.get_instance()
shared_ven_info.set_anget_id(AGENT_ID)
shared_ven_info.set_resource_id(RESOURCE_ID)
shared_ven_info.set_vtn_id(VTN_ID)
shared_ven_info.set_market_interval_in_secondss(MARKET_INTERVAL_IN_SECONDS)


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

    server.app.add_routes([

        web.put('/dispatch/{device_id}', functools.partial(handle_dispatch,
                                                           DISPATCHES_API_URL=DISPATCHES_API_URL)),
        web.put('/order/{device_id}', functools.partial(handle_order,
                ORDERS_API_URL=ORDERS_API_URL)),
        web.put('/meter/{device_id}', functools.partial(handle_meter,
                                                        METERS_API_URL=METERS_API_URL)),
        web.get('/health', handle_health_check)
    ])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(server.run())
    loop.run_forever()
