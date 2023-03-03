import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRClient, enable_default_logging
from api.sonnen_api import SonnenInterface, SonnenBatteryAttributeKey
from api.mock_sonnen_api import MockSonnenInterface

from enum import Enum
import os


class DEVICE_TYPES(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'


DEV = bool(os.getenv('DEV'))
VEN_ID = os.getenv('VEN_ID')
VTN_URL = os.getenv('VTN_URL')
BATTERY_TOKEN = os.getenv('BATTERY_TOKEN')
BATTERY_SN = os.getenv('BATTERY_SN')
DEVICE_ID = os.getenv('DEVICE_ID')
DEVICE_TYPE = os.getenv('DEVICE_TYPE')
TIMEZONE = os.getenv('TIMEZONE')
PRICE_THRESHOLD = os.getenv('PRICE_THRESHOLD')
MOCK_BATTERY_API_URL = os.getenv('MOCK_BATTERY_API_URL')
BATTERY_SN = os.getenv('BATTERY_SN')
INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND = int(
    os.environ['INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND'])

REPORT_SPECIFIER_ID = os.getenv('REPORT_SPECIFIER_ID')
REPORT_DURATION_INSECOND = int(os.environ['REPORT_DURATION_INSECOND'])
print(
    f"DEVICE_TYPE: {DEVICE_TYPE}, DEV :{DEV} MOCK_BATTERY_API_URL: {MOCK_BATTERY_API_URL}")

enable_default_logging()


# start to implement Sonnen API
async def collect_report_value(date_from, date_to, sampling_interval):
    if DEVICE_TYPE == DEVICE_TYPES.SONNEN_BATTERY.value:
        # print(f"BATTERY_SN: {BATTERY_SN}, BATTERY_TOKEN:{BATTERY_TOKEN}, TIMEZONE:{TIMEZONE}")
        try:
            if DEV is not True:
                battery_interface = SonnenInterface(
                    serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
                report_data = battery_interface.get_status_and_convert_to_openleadr_report()
            else:
                print(
                    f"Use mock battery api :{MOCK_BATTERY_API_URL}, auth_token:{BATTERY_TOKEN},serial: {BATTERY_SN}")
                mock_battery_interface = MockSonnenInterface(
                    serial=BATTERY_SN, auth_token=BATTERY_TOKEN, url_ini=MOCK_BATTERY_API_URL)
                report_data = mock_battery_interface.get_status_and_convert_to_openleadr_report()
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
        # requset battery api to control the battery
        if DEVICE_TYPE == DEVICE_TYPES.SONNEN_BATTERY.value:

            try:
                if DEV is not True:
                    battery_interface = SonnenInterface(
                        serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
                    print("Send post requst to contorl the real battery")
                    print("Not implement yet!!")
                    # report_data = battery_interface.get_status_and_convert_to_openleadr_report()
                else:
                    mock_battery_interface = MockSonnenInterface(
                        serial=BATTERY_SN, auth_token=BATTERY_TOKEN, url_ini=MOCK_BATTERY_API_URL)
                    # if we need to implement the mode, change this parameters
                    mode = 2
                    mock_battery_interface.mock_control_battery(mode=mode)
                # print(f"report_data {report_data}")
            except Exception as e:
                raise Exception(f"something wrong: {e}")
        elif DEVICE_TYPE == DEVICE_TYPES.E_GUAGE.value:
            print("Send post requst to contorl the e-guage")
        else:
            raise ValueError('DEVICE_TYPE not found')
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
client = OpenADRClient(ven_name=VEN_ID,
                       vtn_url=VTN_URL)
# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id=DEVICE_ID,
                  report_specifier_id=REPORT_SPECIFIER_ID,
                  data_collection_mode='full',
                  measurement=DEVICE_TYPES.SONNEN_BATTERY.value,
                  # report_duration: The time span that can be provided in this report.
                  report_duration=timedelta(seconds=REPORT_DURATION_INSECOND),
                  sampling_rate=timedelta(seconds=INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND))


# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()
