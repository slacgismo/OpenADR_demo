import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
import logging

enable_default_logging()

enable_default_logging(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openleadr')


async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    logger.debug("====== collect_report_value =======")
    return 1.23


async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    logger.debug(f"=== handle_event ===: {event}")
    return 'optIn'

# Create the client object
client = OpenADRClient(ven_name='ven123',
                       vtn_url='http://0.0.0.0:8080/OpenADR2/Simple/2.0b',
                       debug=True)

# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id='device001',
                  measurement='voltage',
                  report_duration=timedelta(seconds=30),
                  sampling_rate=timedelta(seconds=10))

# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.set_debug(True)
asyncio.set_event_loop(loop)
loop.create_task(client.run())
loop.run_forever()
