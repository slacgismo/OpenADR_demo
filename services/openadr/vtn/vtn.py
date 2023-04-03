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
from actions.on_create_party_registration import on_create_party_registration
logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)


try:
    # The SQS_GROUPID is used to separate the sqs queue for different environment.
    # if you want to send message to AWS worker, the SQS_GROUPID should be set to "AWS"
    # if you want to send message to local worker, the SQS_GROUPID should be set to "LOCAL"
    ENV = os.environ['ENV']
    AGENT_ID = os.environ['AGENT_ID']
    RESOURCE_ID = os.environ['RESOURCE_ID']
    VTN_ID = os.environ['VTN_ID']
    MARKET_INTERVAL_IN_SECOND = os.environ['MARKET_INTERVAL_IN_SECOND']
    METERS_API_URL = os.environ['METERS_API_URL']
    DEVICES_API_URL = os.environ['DEVICES_API_URL']
    ORDERS_PAI_URL = os.environ['ORDERS_PAI_URL']
    DISPATCHES_API_URL = os.environ['DISPATCHES_API_URL']
    MARKET_START_TIME = os.environ['MARKET_START_TIME']
    LOCAL_TIMEZONE = os.environ['LOCAL_TIMEZONE']
except Exception as e:
    raise Exception(f"ENV is not set correctly: {e}")
tz_local = pytz.timezone(LOCAL_TIMEZONE)

# Future db
VENS = {
    "ven0": {
        "ven_name": "ven0",
        "ven_id": "ven0",
        "registration_id": "ven0"
    }
}

# form data lookup for creating an event with the html page


def find_ven(form_data):
    for v in VENS.values():
        logging.info(v['ven_id'])
        if v.get('ven_id') == form_data:
            return True
        else:
            return False


def ven_lookup(ven_id):
    logging.info(f"ven_lookup {ven_id}")
    for v in VENS.values():
        logging.info(v['ven_id'])
        if v.get('ven_id') == ven_id:
            return {'ven_id': v['ven_id'],
                    'ven_name': v['ven_name'],
                    'registration_id': v['registration_id']}
    return {}


if __name__ == "__main__":

    # Create the server object
    server = OpenADRServer(vtn_id='myvtn',
                           http_host='0.0.0.0',
                           ven_lookup=ven_lookup)

    # Add the handler for client (VEN) registrations
    server.add_handler('on_create_party_registration',
                       functools.partial(on_create_party_registration, VENS=VENS, DEVICES_API_URL=DEVICES_API_URL))

    # Add the handler for report registrations from the VEN
    # server.add_handler('on_register_report', on_register_report)

    server.app.add_routes([
        # web.get('/trigger/{minutes_duration}', handle_trigger_event),
        # web.get('/cancel', handle_cancel_event),
        web.put('/order/{ven_id}', functools.partial(handle_order,
                ORDERS_PAI_URL=ORDERS_PAI_URL)),
        web.put('/meter/{ven_id}', functools.partial(handle_meter,
                                                     METERS_API_URL=METERS_API_URL)),
        web.get('/vens', functools.partial(handle_all_ven_info, VENS=VENS)),
        web.get('/health', handle_health_check)
    ])

    # logging.debug(f"Configured server {server}")

    loop = asyncio.new_event_loop()
    # loop.set_debug(True)
    asyncio.set_event_loop(loop)
    loop.create_task(server.run())
    loop.run_forever()
