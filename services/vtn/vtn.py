

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
    Consumption_Avg = 3
    Consumption_W = 4
    Fac = 5
    FlowConsumptionBattery = 6
    FlowConsumptionGrid = 7
    FlowConsumptionProduction = 8
    FlowGridBattery = 9
    FlowProductionBattery = 10
    FlowProductionGrid = 11
    GridFeedIn_W = 12
    IsSystemInstalled = 13
    OperatingMode = 14
    Pac_total_W = 15
    Production_W = 16
    RSOC = 17
    RemainingCapacity_W = 18
    SystemStatus = 19
    USOC = 20
    Uac = 21
    Ubat = 22
    Timestamp = "Timestamp"


class DEVICE_TYPES(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'


TIMEZONE = os.environ['TIMEZONE']
GET_VENS_URL = os.environ['GET_VENS_URL']
SAVE_DATA_URL = os.environ['SAVE_DATA_URL']


tz_local = pytz.timezone(TIMEZONE)

if __name__ == "__main__":
    pass

enable_default_logging(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('openleadr')

logger.info("vtn at top")

# Future db
# VENS = {
#     "ven123": {
#         "ven_name": "ven123",
#         "ven_id": "ven_id_ven123",
#         "registration_id": "reg_id_ven123"
#     }
# }
VENS = {}
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
        params = {"NAME": ven_name}
        url = GET_VENS_URL
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

        message = response_json.get('message')c
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
    logger.info(f"ven_lookup {ven_id}")
    for v in VENS.values():
        # logger.debug(v['ven_id'])
        if v.get('ven_id') == ven_id:
            return {'ven_id': v['ven_id'],
                    'ven_name': v['ven_name'],
                    'registration_id': v['registration_id']}
    return {}


async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    logger.debug(
        f"TRYING TO LOOK UP VEN FOR REGISTRATION: {registration_info['ven_name']}")

    ven_name = registration_info['ven_name']
    for v in VENS.values():
        # print(values['ven_name'])
        if v.get('ven_name') == ven_name:
            # logger.debug(
            #     f"REGISTRATION SUCCESS WITH NAME:  {v.get('ven_name')} FROM PAYLOAD, MATCH FOUND {ven_name}")
            return v['ven_id'], v['registration_id']
    print("****************")
    print("Cannot find ven_name, try to fetch from url")
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

    print("---------------")
    print("get report and send to the post url")
    send_report_data_to_url(url=SAVE_DATA_URL, data=josn_report)


async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """

    logger.info(
        f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")


async def handle_cancel_event(request):
    """
    Handle a cancel event request.
    """
    try:
        server = request.app["server"]
        server.cancel_event(ven_id='ven_id_ven123',
                            event_id="our-event-id",
                            )

        datetime_local = datetime.now(tz_local)
        datetime_local_formated = datetime_local.strftime("%H:%M:%S")
        info = f"Event canceled now, local time: {datetime_local_formated}"
        response_obj = {'status': 'success', 'info': info}

        # return sucess
        return web.json_response(response_obj)

    except Exception as e:

        response_obj = {'status': 'failed', 'info': str(e)}

        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)


async def handle_trigger_event(request):

    try:
        data = await request.json()
        # Check if the body exists and is in the correct format
        if not data or not isinstance(data, dict):
            return web.json_response({'status': 'error', 'message': 'Invalid request body'}, status=400)

        # Pase data
        price = data['price']
        ven_ids = data['ven_ids']
        minutes_duration = data['minutes_duration']

        for ven_id in ven_ids:
            server.add_event(ven_id=ven_id,
                             signal_name=enums.SIGNAL_NAME.simple,
                             signal_type=enums.SIGNAL_TYPE.LEVEL,
                             intervals=[{'dtstart': datetime.now(timezone.utc),
                                        'duration': timedelta(minutes=int(minutes_duration)),
                                         'signal_payload': price}],
                             callback=event_response_callback,
                             event_id="our-event-id",
                             )

        return web.json_response({'status': 'success'})
    except json.JSONDecodeError:
        return web.json_response({'status': 'error', 'message': 'Invalid JSON format'}, status=400)


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

logger.debug("vtn before OpenADRServer")

# Create the server object
server = OpenADRServer(vtn_id='myvtn',
                       http_host='0.0.0.0')
# ven_lookup=ven_lookup)

logger.debug(f"vtn created server {server}")

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration',
                   on_create_party_registration)

logger.debug(f"vtn add_handler on_create_party_registration")

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

logger.debug(f"vtn add_handler on_register_report")


server.app.add_routes([
    # web.get('/trigger/{minutes_duration}', handle_trigger_event),
    web.post('/api/v1.0/trigger_events', handle_trigger_event),
    web.get('/cancel', handle_cancel_event),
    web.get('/vens', all_ven_info)
])


logger.debug(f"Configured server {server}")

loop = asyncio.new_event_loop()
# loop.set_debug(True)
asyncio.set_event_loop(loop)
loop.create_task(server.run())
# Using this line causes failure
# asyncio.run(server.run(), debug=True)
loop.run_forever()
