import asyncio
import logging
from aiohttp import web
import logging
import aiohttp
from classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS
from .handle_order import sumbit_oder_to_oder_api
import time


async def handle_meter(request, METER_API_URL, MARKET_INTERVAL_IN_SECONDS):
    """
    Handle a meter.
    """
    status = None
    response_obj = {'status': status}
    try:
        ven_id = request.match_info['ven_id']
        data = await request.json()
        logging.info("=====================================")
        logging.info(f"handle_meter: {ven_id}")
        logging.info("=====================================")
        if 'device_id' not in data or 'meter_id' not in data or 'resource_id' not in data or 'device_data' not in data or 'device_type' not in data or 'device_brand' not in data:
            raise Exception(f"Error parse meter data: {data}")
        logging.info("Convert device data to meter data")
        device_data = data['device_data']
        device_id = data['device_id']
        meter_id = data['meter_id']
        device_type = data['device_type']
        resource_id = data['resource_id']
        device_brand = data['device_brand']
        real_energy, reactive_energy, real_power, reactive_power = convert_device_data_to_meter_data(
            device_type=device_type,
            device_brand=device_brand,
            market_interval_in_seconds=MARKET_INTERVAL_IN_SECONDS,
            device_data=device_data)

        meter_url = METER_API_URL + "/" + device_id + "/" + meter_id

        meter_data = {
            "resource_id": resource_id,
            "real_energy": real_energy,
            "reactive_energy": reactive_energy,
            "real_power": real_power,
            "reactive_power": reactive_power,
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(meter_url, json=meter_data) as meter_response:
                content_type = meter_response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    raise Exception(f"Unexpected content type: {content_type}")
        if meter_response.status == 200:
            logging.info("=====================================")
            logging.info(f"send to meter api success")
            logging.info("=====================================")
            response_obj = {'status': 'success'}
            return web.json_response(response_obj, status=200)
        else:
            logging.info("=====================================")
            logging.info(f"send to meter api failed")
            logging.info("=====================================")
            response_obj = {'status': 'failed'}
            return web.json_response(response_obj, status=500)

    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)


def convert_device_data_to_meter_data(
        device_type: str = None,
        device_brand: str = None,
        market_interval_in_seconds: int = None,
        device_data: dict = None):

    if device_type == DEVICE_TYPES.ES.value:
        if device_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
            # real power
            real_power = device_data['Pac_total_W']
            # real energy
            market_interval_in_minutes = market_interval_in_seconds/60
            market_interval_in_hour = 60/market_interval_in_minutes
            real_energy = real_power/market_interval_in_hour
            # not measured
            reactive_energy = None
            reactive_power = None
        else:
            logging.error(f"Not supported device brand: {device_brand}")
    else:
        logging.error(f"Not supported device type: {device_type}")
    return real_energy, reactive_energy, real_power, reactive_power


# async def submit_meter_to_meter_url(
#     device_id: str = None,
#     meter_id: str = None,
#     resource_id: str = None,
#     real_energy: str = None,
#     reactive_energy: str = None,
#     real_power: str = None,
#     reactive_power: str = None,
#     METER_API_URL: str = None,
# ):
#     """
#     Submit the oder_id to dispatch and await for the response
#     The response will be a quantity of the POWER
#     PUT /meter/{device_id}/{meter_id}
#     """

#     meter_url = METER_API_URL + "/" + device_id + "/" + meter_id
#     print(f"send device data to TESS meter  api: {device_id}/{meter_id}")
#     data = {
#         "resource_id": resource_id,
#         "real_energy": real_energy,
#         "reactive_energy": reactive_energy,
#         "real_power": real_power,
#         "reactive_power": reactive_power,
#     }
#     print(
#         f"send device data to TESS meter  api: {device_id}/{meter_id}")
#     async with aiohttp.ClientSession() as session:
#         async with session.put(meter_url, json=data) as response:
#             content_type = response.headers.get('Content-Type', '')
#             if 'application/json' not in content_type:
#                 raise Exception(f"Unexpected content type: {content_type}")
#             try:
#                 body = await response.json()
#                 print(f"meter response: {body}")
#             except Exception as e:
#                 raise Exception(f"Error parse response: {e}")
#             return response
