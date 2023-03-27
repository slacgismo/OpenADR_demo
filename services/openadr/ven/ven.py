import aiohttp
import asyncio
from datetime import timedelta
import pytz
from openleadr import OpenADRClient, enable_default_logging
import os
import logging
from models_classes.HTTPServer import HTTPServer

VTN_ADDRESS = os.environ['VTN_ADDRESS']
VTN_PORT = os.environ['VTN_PORT']
RESOURCE_NAME = "resource123"
VEN_NAME = "ven123"
HTTPSERVER_PORT = 8000

VEN_ID = VEN_NAME + "_id"

tz_local = pytz.timezone('America/Chicago')


if __name__ == "__main__":
    # code here
    pass

enable_default_logging(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openleadr')
vtn_url = f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b"
logger.debug(f"VEN START {VEN_NAME} {vtn_url} {RESOURCE_NAME} {VEN_ID}")


async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    logger.debug("collect_report_value")
    return 1.23


async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    logger.debug(f"handle_event {event}")
    return 'optIn'

# Create the client object
client = OpenADRClient(
    ven_name=VEN_NAME, vtn_url=f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b", debug=True)
# , ven_id=VEN_ID

# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id=RESOURCE_NAME,
                  measurement='voltage',
                  sampling_rate=timedelta(seconds=60))

# Add event handling capability to the client
client.add_handler('on_event', handle_event)

logger.debug("After add_handler on_event")


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
