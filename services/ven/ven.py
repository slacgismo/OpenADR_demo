import requests
import subprocess  # For executing a shell command
import platform    # For getting the operating system name
import asyncio
from datetime import datetime, timedelta
from openleadr import OpenADRClient, enable_default_logging
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
import time
import socket
import os
from device_type_enum import DEVICE_TYPES

# get environment variables
ENV = os.getenv('ENV')

print("ENV: ", ENV)
VEN_ID = os.getenv('VEN_ID')
# VTN_URL = os.getenv('VTN_URL')
VTN_ADDRESS = os.getenv('VTN_ADDRESS')
VTN_PORT = os.getenv('VTN_PORT')
BATTERY_TOKEN = os.getenv('BATTERY_TOKEN')
BATTERY_SN = os.getenv('BATTERY_SN')
DEVICE_ID = os.getenv('DEVICE_ID')
DEVICE_TYPE = os.getenv('DEVICE_TYPE')
PRICE_THRESHOLD = os.getenv('PRICE_THRESHOLD')
MOCK_DEVICES_API_URL = os.getenv('MOCK_DEVICES_API_URL')
BATTERY_SN = os.getenv('BATTERY_SN')
INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND = int(
    os.environ['INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND'])


enable_default_logging()


# async def collect_report_value(date_from, date_to, sampling_interval):
#     fetch_devices_data(device_type=DEVICE_TYPE)


async def collect_report_value(date_from, date_to, sampling_interval):

    try:
        if DEVICE_TYPE == DEVICE_TYPES.SONNEN_BATTERY.value:

            if ENV == 'PROD':
                battery_interface = SonnenInterface(
                    serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
                report_data = battery_interface.get_status_and_convert_to_openleadr_report()

                return report_data
            elif ENV == 'DEV':

                print(
                    f"Use mock battery api :{MOCK_DEVICES_API_URL}, auth_token:{BATTERY_TOKEN},serial: {BATTERY_SN}")
                mock_battery_interface = MockSonnenInterface(
                    serial=BATTERY_SN, auth_token=BATTERY_TOKEN, url_ini=MOCK_DEVICES_API_URL)
                report_data = mock_battery_interface.get_status_and_convert_to_openleadr_report()

                return report_data
                # print(f"report_data {report_data}")
            else:
                raise ValueError('ENV not found: ', ENV)

        elif DEVICE_TYPE == DEVICE_TYPES.E_GUAGE.value:
            # get data from e gauate api
            return 1.23
        else:
            raise ValueError('DEVICE_TYPE not found')
    except Exception as e:
        raise Exception(f"something wrong: {e}")


def control_real_device(device_type: DEVICE_TYPES, device_id: str, value: float):
    """
    Control the device by the value
    param: device_type: DEVICE_TYPES
    param: device_id: str
    param: value: float
    """
    print(" ---- control device ----")
    # requset battery api to control the battery
    try:
        if device_type == DEVICE_TYPES.SONNEN_BATTERY.value:

            battery_interface = SonnenInterface(
                serial=BATTERY_SN, auth_token=BATTERY_TOKEN)
            print("Send post requst to contorl the real battery")
            print("********* Not implement yet!! **************")

        elif DEVICE_TYPE == DEVICE_TYPES.E_GUAGE.value:
            print("Send post requst to contorl the e-guage")
        else:
            raise ValueError('DEVICE_TYPE not found')
    except Exception as e:
        raise Exception(f"something wrong: {e}")


def emulate_control_device(device_type: DEVICE_TYPES, device_id: str, value: float):

    try:
        if device_type == DEVICE_TYPES.SONNEN_BATTERY.value:

            print("Send post requst to contorl the mock battery")
            mock_battery_interface = MockSonnenInterface(
                serial=BATTERY_SN, auth_token=BATTERY_TOKEN, url_ini=MOCK_DEVICES_API_URL)
            # if we need to implement the mode, change this parameters
            mode = 2
            mock_battery_interface.mock_control_battery(mode=mode)

        elif DEVICE_TYPE == DEVICE_TYPES.E_GUAGE.value:
            print("Send post requst to contorl the e-guage")
        else:
            raise ValueError('DEVICE_TYPE not found')
    except Exception as e:
        raise Exception(f"something wrong: {e}")


def decide_participate_market_by_price(market_price: float, price_threshold: float = 0.15):
    if market_price >= price_threshold:
        print(
            f"{VEN_ID} participates market: market_price: {market_price} price_threshold:{price_threshold}")
        if ENV == "PROD":
            control_real_device(device_type=DEVICE_TYPE,
                                device_id=DEVICE_ID, value=market_price)
        elif ENV == "DEV":
            emulate_control_device(
                device_type=DEVICE_TYPE, device_id=DEVICE_ID, value=market_price)
        else:
            raise ValueError('DEV or PROD not found: ', ENV)

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


def check_server_health(api_link):
    try:
        response = requests.get(api_link)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    # check if the server is up
    is_server_up = False
    retry_count = 0
    # retry 3 times
    while retry_count < 3:
        is_server_up = check_server_health(
            api_link=f"http://{VTN_ADDRESS}:{VTN_PORT}/health")
        if is_server_up:
            print("server is up")
            break
        else:
            time.sleep(2)
            print("Server is not up, wait 2 seconds")
        retry_count += 1

    if not is_server_up:
        raise Exception("Server is not up, exit the program")

    client = OpenADRClient(ven_name=VEN_ID,
                           vtn_url=f"http://{VTN_ADDRESS}:{VTN_PORT}/OpenADR2/Simple/2.0b")
    # Add the report capability to the client
    client.add_report(callback=collect_report_value,
                      resource_id=DEVICE_ID,
                      report_specifier_id=DEVICE_TYPES.SONNEN_BATTERY.value,
                      data_collection_mode='full',
                      measurement=DEVICE_TYPES.SONNEN_BATTERY.value,
                      # report_duration: The time span that can be provided in this report default=3600.
                      report_duration=timedelta(seconds=3600),
                      sampling_rate=timedelta(seconds=INTERVAL_OF_FETCHING_DEVICE_DATA_INSECOND))

    # Add event handling capability to the client
    client.add_handler('on_event', handle_event)

    # Run the client in the Python AsyncIO Event Loop
    loop = asyncio.get_event_loop()
    loop.create_task(client.run())
    loop.run_forever()
