

import asyncio
from datetime import datetime, timezone, timedelta
import pytz
from openleadr import OpenADRServer, enable_default_logging
from openleadr.utils import generate_id
from functools import partial
from aiohttp import web
import os
import logging
from openleadr import objects, enums, utils
from enum import Enum
import json
import requests
import aiohttp
import uuid


class SonnenBatteryOperatingMode(Enum):
    TimeofUseMode = 10
    ManualMode = 1
    SelfConsumptionMode = 2
    BackupMode = 7


class SonnenBatterySystemStatus(Enum):
    OnGrid = 1
    OffGrid = 0


class SonnenBatteryAttributeKey(Enum):
    BackupBuffer = 0
    BatteryCharging = 1
    BatteryDischarging = 2
    # Consumption_Avg # exist but unused data
    Consumption_W = 3
    Fac = 4
    FlowConsumptionBattery = 5
    FlowConsumptionGrid = 6
    FlowConsumptionProduction = 7
    FlowGridBattery = 8
    FlowProductionBattery = 9
    FlowProductionGrid = 10
    GridFeedIn_W = 11
    # IsSystemInstalled  # exist but unused data
    OperatingMode = 12
    Pac_total_W = 13
    Production_W = 14
    # RSOC # exist but unused data
    RemainingCapacity_W = 15
    SystemStatus = 16
    USOC = 17
    Uac = 18
    Ubat = 19
    Timestamp = 'Timestamp'


class DEVICE_TYPES(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'


TIMEZONE = os.environ['TIMEZONE']
GET_VENS_URL = os.environ['GET_VENS_URL']
VTN_ID = os.environ['VTN_ID']
SAVE_DATA_URL = os.environ['SAVE_DATA_URL']
MARKET_PRICES_URL = os.environ['MARKET_PRICES_URL']
PARTICIPATED_VENS_URL = os.environ['PARTICIPATED_VENS_URL']
INTERVAL_OF_FETCHING_MARKET_PRICE_INSECOND = int(
    os.environ['INTERVAL_OF_FETCHING_MARKET_PRICE_INSECOND'])
tz_local = pytz.timezone(TIMEZONE)

if __name__ == "__main__":
    pass

# enable_default_logging(level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('openleadr')

# logger.info("vtn at top")

# Future db
VENS = {
    "ven789": {
        "ven_name": "ven789",
        "ven_id": "ven789",
        "registration_id": "reg_id_ven789"
    }
}
# VENS = {}
# form data lookup for creating an event with the html page


def send_report_data_to_url(url: str, data: dict) -> bool:
    try:
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise ValueError(
                f'Request failed with status {response.status_code}')
        response_json = response.json()
        # print(f"response_json: {response_json}")
        return True
    except Exception as e:
        raise e


def check_if_ven_exist_in_tess_db(ven_url: str, ven_name: str) -> bool:
    try:
        print(f"ven_url :{ven_url}, ven_name:{ven_name}")
        params = {"NAME": ven_name}
        url = ven_url
        response = requests.get(
            url,
            params=params
        )
        # print(f"000 url {url}")
        # print(f"response:{response}")
        if response.status_code != 200:
            raise ValueError(
                f'Request failed with status {response.status_code}')
        response_json = response.json()
        print(f"response_json: {response_json}")

        message = response_json.get('message')
        print(f"body: {message}")
        if not message:
            raise ValueError('Response body is missing or empty')
        # # if "message" in body:
        if ven_name in message:
            # print("find ven ")
            ven_info = message[ven_name]
            VENS[ven_name] = ven_info
            # print("======================")
            # print(f"VEN {VENS}")
            return ven_info['ven_id'], ven_info['registration_id'],
        else:
            return False

    except Exception as e:
        raise e


def find_ven(form_data):
    for v in VENS.values():
        # logger.debug(v['ven_id'])
        if v.get('ven_id') == form_data:
            return True
        else:
            return False


def ven_lookup(ven_id):
    # logger.info(f"ven_lookup {ven_id}")
    for v in VENS.values():
        # logger.debug(v['ven_id'])
        if v.get('ven_id') == ven_id:
            return {'ven_id': v['ven_id'],
                    'ven_name': v['ven_name'],
                    'registration_id': v['registration_id']}
    return {}


def post_participated_vens_to_api(api_url: str, ven_id: str):
    """
    Periodically fetch data from a REST API URL using requests package.
    """
    try:
        payload = {"ven_id": ven_id}
        response = requests.post(api_url, json=payload)
        # resp = response.json()
        if response.status_code == 200:
            print("-----------")

            print(
                f'****** vtn:{VTN_ID} call TESS and notify ven_id: {ven_id} join market ****')
        else:
            print(f'API call failed with error code {response.status_code}')
        # print("--------*****")
        # print(f"post participated ven : {resp}")
        # print("--------******")
    except Exception as e:
        print(f"error: {e}")


async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    # logger.debug(
    #     f"TRYING TO LOOK UP VEN FOR REGISTRATION: {registration_info['ven_name']}")

    ven_name = registration_info['ven_name']
    for v in VENS.values():
        # print(values['ven_name'])
        if v.get('ven_name') == ven_name:
            # logger.debug(
            #     f"REGISTRATION SUCCESS WITH NAME:  {v.get('ven_name')} FROM PAYLOAD, MATCH FOUND {ven_name}")
            return v['ven_id'], v['registration_id']

    print(f"vtn:{VTN_ID} cannot find ven_name, try to fetch from url")
    return check_if_ven_exist_in_tess_db(ven_url=GET_VENS_URL, ven_name=ven_name)


async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    # logger.debug(f"on_register_report {ven_id} {resource_id} {measurement}")

    if measurement == DEVICE_TYPES.SONNEN_BATTERY.value:
        callback = partial(on_update_sonnen_battery_report, ven_id=ven_id,
                           resource_id=resource_id, measurement=measurement)
        sampling_interval = min_sampling_interval
        return callback, sampling_interval
    else:
        pass


async def on_update_sonnen_battery_report(data, ven_id, resource_id, measurement):

    index = 0
    josn_report = {}
    # josn_report[SonnenBatteryAttributeKey.Timestamp.name] =
    if len(data) > len(SonnenBatteryAttributeKey):
        raise ValueError(
            f"Length of data is larger to SonnenBatteryAttributeKey")

    for time, value in data:
        if SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.SystemStatus.name:
            # convert back to OnGrid or OffGrid
            if int(value) == 1:
                josn_report[SonnenBatteryAttributeKey(
                    index).name] = SonnenBatterySystemStatus.OnGrid.name
            elif int(value) == 0:
                josn_report[SonnenBatteryAttributeKey(
                    index).name] = SonnenBatterySystemStatus.OffGrid.name
            else:
                raise ValueError(
                    f"Woops! convert to SonnenBatterySystemStatus fail {value}")

        elif (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.BatteryCharging.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.BatteryDischarging.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowConsumptionBattery.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowConsumptionGrid.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowConsumptionProduction.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowGridBattery.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowProductionBattery.name) \
                or (SonnenBatteryAttributeKey(index).name == SonnenBatteryAttributeKey.FlowProductionGrid.name):
            # convert integert to boolean in the specific attributes
            if int(value) == 1:
                josn_report[SonnenBatteryAttributeKey(index).name] = True
            elif int(value) == 0:
                josn_report[SonnenBatteryAttributeKey(index).name] = False
            else:
                raise ValueError(f"Woops! convert to boolean fail {value}")
        else:
            josn_report[SonnenBatteryAttributeKey(index).name] = value

        josn_report[SonnenBatteryAttributeKey.Timestamp.name] = time.strftime(
            "%Y-%m-%d %H:%M:%S")

        index += 1
    # add ven_id to the report
    josn_report['ven_id'] = ven_id
    # add vtn_id to the report
    josn_report['vtn_id'] = VTN_ID
    print(
        f"******* vtn:{VTN_ID} get report from  {ven_id} send to the TESS *******")
    send_report_data_to_url(url=SAVE_DATA_URL, data=josn_report)


async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    if opt_type == 'optIn':

        print(
            f"***** vtn:{VTN_ID}  ven_id  :{ven_id} opt_type: {opt_type} join the market *******")

        post_participated_vens_to_api(
            api_url=PARTICIPATED_VENS_URL, ven_id=ven_id)


# async def handle_cancel_event(request):
#     """
#     Handle a cancel event request.
#     """
#     try:
#         server = request.app["server"]
#         server.cancel_event(ven_id='ven_id_ven123',
#                             event_id="our-event-id",
#                             )

#         datetime_local = datetime.now(tz_local)
#         datetime_local_formated = datetime_local.strftime("%H:%M:%S")
#         info = f"Event canceled now, local time: {datetime_local_formated}"
#         response_obj = {'status': 'success', 'info': info}

#         # return sucess
#         return web.json_response(response_obj)

#     except Exception as e:

#         response_obj = {'status': 'failed', 'info': str(e)}

#         # return failed with a status code of 500 i.e. 'Server Error'
#         return web.json_response(response_obj, status=500)


async def all_ven_info(request):
    """
    Handle a trigger event request.
    """
    try:
        return web.json_response(VENS)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)

# logger.debug("vtn before OpenADRServer")

# Create the server object
server = OpenADRServer(vtn_id=VTN_ID,
                       http_host='0.0.0.0')
# ven_lookup=ven_lookup)

# logger.debug(f"vtn created server {server}")

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration',
                   on_create_party_registration)

# logger.debug(f"vtn add_handler on_create_party_registration")

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

# logger.debug(f"vtn add_handler on_register_report")


server.app.add_routes([
    # web.get('/trigger/{minutes_duration}', handle_trigger_event),
    # web.post('/api/v1.0/trigger_events', handle_trigger_event),
    # web.get('/cancel', handle_cancel_event),
    web.get('/vens', all_ven_info)
])


async def get_data_from_api():
    """
    Asynchronous function that sends an HTTP GET request to an API and returns the response.
    """
    market_prices_url = MARKET_PRICES_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(market_prices_url) as response:
            data = await response.json()
            return data


async def periodic_function():
    """
    Periodically fetch data from a REST API URL using requests package.
    """

    while True:

        payload = await get_data_from_api()
        message = json.loads(payload['message'])
        market_prices = message['market_prices']
        print(
            f"***** Fetched market_prices from API: {market_prices} ******* ")

        minutes_duration = 1
        for v in VENS.values():
            event_id = str(uuid.uuid4())
            server.add_event(ven_id=v['ven_id'],
                             signal_name=enums.SIGNAL_NAME.simple,
                             signal_type=enums.SIGNAL_TYPE.LEVEL,
                             intervals=[{'dtstart': datetime.now(timezone.utc),
                                        'duration': timedelta(minutes=int(minutes_duration)),
                                         'signal_payload': market_prices}],
                             callback=event_response_callback,
                             event_id=event_id,
                             )
        # Wait for x seconds before fetching the next market price
        await asyncio.sleep(INTERVAL_OF_FETCHING_MARKET_PRICE_INSECOND)

# logger.debug(f"Configured server {server}")

loop = asyncio.new_event_loop()
# loop.set_debug(True)
asyncio.set_event_loop(loop)
# loop.create_task(server.run())
loop.create_task(server.run())
loop.create_task(periodic_function())
# Using this line causes failure
# asyncio.run(server.run(), debug=True)
loop.run_forever()
