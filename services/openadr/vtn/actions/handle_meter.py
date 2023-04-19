import asyncio
import logging
from aiohttp import web
import logging
import aiohttp


import time
from enum import Enum


async def handle_meter(request, METERS_API_URL):
    """
    Handle a meter.
    "readings": device_data,
    "device_id": device_id,
    "meter_id": meter_id,
    "resource_id": resource_id,
    "device_brand": device_brand,
    "status": status
    """

    status = None
    response_obj = {'status': status}
    try:
        device_id = request.match_info['device_id']
        data = await request.json()
        logging.info("=====================================")
        logging.info(f"handle_meter: {device_id}")
        logging.info("=====================================")
        if 'device_id' not in data or 'meter_id' not in data or 'resource_id' not in data or 'readings' not in data or 'device_brand' not in data:
            raise Exception(f"Error parse meter data: {data}")
        logging.info("Convert device data to meter data")
        readings = data['readings']
        device_id = data['device_id']
        meter_id = data['meter_id']
        resource_id = data['resource_id']
        device_brand = data['device_brand']
        status = data['status']
        timestamp = data['timestamp']
        meter_url = METERS_API_URL + "/" + device_id + "/" + meter_id
        meter_data = {
            "resource_id": resource_id,
            "readings": readings,
            "device_id": device_id,
            "device_brand": device_brand,
            "status": status,
            "timestamp": timestamp
        }
        logging.info("=====================================")
        logging.info(f"send to meter url: {meter_url}")
        logging.info(f"send to meter data: {meter_data}")
        logging.info("=====================================")

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
        logging.error(f"get meter data failed {e}")
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)
