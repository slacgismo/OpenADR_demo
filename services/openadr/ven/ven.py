import aiohttp
import asyncio
from datetime import timedelta
import pytz
from openleadr import OpenADRClient, enable_default_logging
import os
import logging
from models_classes.HTTPServer import HTTPServer
try:
    ENV = os.environ['ENV']
    VEN_ID = os.environ['VEN_ID']
    RESOURCE_ID = os.environ['RESOURCE_ID']
    METER_ID = os.environ['METER_ID']
    DEVICE_ID = os.environ['DEVICE_ID']
    AGENT_ID = os.environ['AGENT_ID']
    DEVICE_NAME = os.environ['DEVICE_NAME']

    VTN_ADDRESS = os.environ['VTN_ADDRESS']
    VTN_PORT = os.environ['VTN_PORT']
    DEVICE_TYPE = os.environ['DEVICE_TYPE']
    EMULATED_DEVICE_API_URL = os.environ['EMULATED_DEVICE_API_URL']
    MARKET_INTERVAL_IN_SECOND = os.environ['MARKET_INTERVAL_IN_SECOND']
    FLEXIBLE = os.environ['FLEXIBLE']
    MARKET_START_TIME = os.environ['MARKET_START_TIME']
    LOCAL_TIMEZONE = os.environ['LOCAL_TIMEZONE']
    HTTPSERVER_PORT = os.environ['HTTPSERVER_PORT']
except Exception as e:
    raise Exception(f"ENV is not set correctly: {e}")

logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)
# enable_default_logging(level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('openleadr')
vtn_url = f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b"
logging.debug(f"VEN START {VEN_ID} {vtn_url} {RESOURCE_ID} {VEN_ID}")


async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    logging.debug("collect_report_value")
    return 1.23


async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    logging.debug(f"handle_event {event}")
    return 'optIn'

if __name__ == "__main__":
    # code here
    pass
    # Create the client object
    client = OpenADRClient(
        ven_name=VEN_ID, vtn_url=f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b", debug=True)
    # , ven_id=VEN_ID

    # Add the report capability to the client
    client.add_report(callback=collect_report_value,
                      resource_id=RESOURCE_ID,
                      measurement='voltage',
                      sampling_rate=timedelta(seconds=60))

    # Add event handling capability to the client
    client.add_handler('on_event', handle_event)

    logging.debug("After add_handler on_event")

    simple_server = HTTPServer(
        healthcheck_port=HTTPSERVER_PORT, ven_id=VEN_ID
    )
    loop = asyncio.get_event_loop()
    loop.create_task(simple_server.start())
    loop.create_task(client.run())
    loop.create_task(simple_server.check_thirdparty_api(
        thirdparty_api_url="https://google.com", interval=60
    ))
    loop.run_forever()
