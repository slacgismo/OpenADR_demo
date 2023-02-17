import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging
from api.sonnen_api import SonnenInterface
# from models.SonnenBattery import SonnenBatteryAttributeKey
import os

VEN_NAME = os.getenv('VEN_NAME')
VTN_URL = os.getenv('VTN_URL')
BATTERY_TOKEN = os.getenv('BATTERY_TOKEN')
BATTERY_SN = os.getenv('BATTERY_SN')
DEVICE_ID = os.getenv('DEVICE_ID')
enable_default_logging()


async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    # battery_interface = SonnenInterface(
    #     serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
    # batt_staus = battery_interface.get_status()
    # Consumption_W = batt_staus['Consumption_W']
    # return Consumption_W
    return 1.23


async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    print(f"********* price event:{event}\n")
    return 'optIn'

# Create the client object
# client = OpenADRClient(ven_name='ven123',
#                        vtn_url='http://vtn:8080/OpenADR2/Simple/2.0b')
client = OpenADRClient(ven_name=VEN_NAME,
                       vtn_url=VTN_URL)
# Add the report capability to the client
# client.add_report(callback=collect_report_value,
#                   resource_id=DEVICE_ID,
#                   measurement="hello",
#                   report_duration=timedelta(seconds=30),
#                   sampling_rate=timedelta(seconds=30))

# client.add_report(callback=collect_report_value,
#                   resource_id=DEVICE_ID,
#                   measurement=SonnenBatteryAttributeKey.BackupBuffer,
#                   report_duration=timedelta(seconds=30),
#                   sampling_rate=timedelta(seconds=30))

# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()
