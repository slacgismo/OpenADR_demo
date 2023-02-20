import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRClient, enable_default_logging
from api.sonnen_api import SonnenInterface, SonnenBatteryAttributeKey


from enum import Enum
import os


class DEVICE_TYPES(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'


VEN_NAME = os.getenv('VEN_NAME')
VTN_URL = os.getenv('VTN_URL')
BATTERY_TOKEN = os.getenv('BATTERY_TOKEN')
BATTERY_SN = os.getenv('BATTERY_SN')
DEVICE_ID = os.getenv('DEVICE_ID')
DEVICE_TYPE = os.getenv('DEVICE_TYPE')
TIMEZONE = os.environ['TIMEZONE']
PRICE_THRESHOLD = os.environ['PRICE_THRESHOLD']
print(f"DEVICE_TYPE: {DEVICE_TYPE}")

enable_default_logging()


# start to implement Sonnen API
async def collect_report_value(date_from, date_to, sampling_interval):
    if DEVICE_TYPE == DEVICE_TYPES.SONNEN_BATTERY.value:
        # print(f"BATTERY_SN: {BATTERY_SN}, BATTERY_TOKEN:{BATTERY_TOKEN}, TIMEZONE:{TIMEZONE}")
        try:
            battery_interface = SonnenInterface(
                serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
            report_data = battery_interface.get_status_and_convert_to_openleadr_report()
            # print(f"report_data {report_data}")
        except Exception as e:
            raise Exception(f"something wrong: {e}")
        return report_data
        # datetime_str = '2023-02-09 14:50:32'
        # datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # return [(datetime_object, 10.0),(datetime_object, 11.0)]

    elif DEVICE_TYPE == DEVICE_TYPES.E_GUAGE.value:
        # get data from e gauate api
        return 1.23
    else:
        raise ValueError('DEVICE_TYPE not found')


def decide_participate_market_by_price(market_price: float, price_threshold: float = 0.15):
    if market_price >= price_threshold:
        print("-----------")
        print(
            f"Participate market: market_price: {market_price} price_threshold:{price_threshold}")
        print("-----------")
    else:
        print(
            f"Not participate  market_price: {market_price} price_threshold:{price_threshold}")


async def handle_event(event):
    """
    Get event from VTN 
    The raw data:


    """
    try:
        print(f"event :{event}")
        event_descriptor = event['event_descriptor']
        event_signals = event['event_signals']

        if event_signals:
            for signal in event_signals:
                signal_payload = signal.get('intervals')[
                    0].get('signal_payload')
                if signal_payload is not None:
                    market_price = float(signal_payload)
                    decide_participate_market_by_price(
                        market_price=market_price, price_threshold=float(PRICE_THRESHOLD))

    except (ValueError, TypeError, IndexError) as e:
        print(f"Woops!! key error:{e}")

    return 'optIn'

# Create the client object
# client = OpenADRClient(ven_name='ven123',
#                        vtn_url='http://vtn:8080/OpenADR2/Simple/2.0b')
client = OpenADRClient(ven_name=VEN_NAME,
                       vtn_url=VTN_URL)
# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id=DEVICE_ID,
                  report_specifier_id='BatteryReport',
                  data_collection_mode='full',
                  measurement=DEVICE_TYPES.SONNEN_BATTERY.value,
                  report_duration=timedelta(seconds=3600),
                  sampling_rate=timedelta(seconds=10))


# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()
