import asyncio
import logging
from aiohttp import web
import logging


async def handle_meter(request, METERS_API_URL):
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
        # Do something with the parsed JSON data
        # meter_response = await submit_meter_to_meter_url(data=data, METERS_API_URL=METERS_API_URL)
        # if meter_response.status == 200:
        #     logging.info("send to meter api success")
        response_obj = {'status': 'success'}
        return web.json_response(response_obj, status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)


async def submit_meter_to_meter_url(
    data: dict,
    METERS_API_URL: str,
):
    logging.info("=====================================")
    logging.info(f"TODO:submit_meter_to_meter_url: {data}")
    logging.info("=====================================")
    response_obj = {'status': 'failed'}
    return web.json_response(response_obj, status=200)
