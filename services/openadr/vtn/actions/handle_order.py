import asyncio
import logging
from aiohttp import web
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp
from utils.guid import guid
from .handle_event import send_price_to_ven_through_openadr_event, send_quantity_to_ven_through_openadr_event
from enum import Enum


class ORER_KEYS(Enum):
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    METER_ID = 'meter_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'


def parse_order_data(data: dict):
    try:
        device_id = data[ORER_KEYS.DEVICE_ID.value]
        meter_id = data[ORER_KEYS.METER_ID.value]
        resource_id = data[ORER_KEYS.RESOURCE_ID.value]
        record_time = data[ORER_KEYS.RECORD_TIME.value]
        flexible = data[ORER_KEYS.FLEXIBLE.value]
        state = data[ORER_KEYS.STATE.value]
    except Exception as e:
        raise Exception(f"Error parse order data: {e}")
    # state can be None ??
    return device_id, meter_id, resource_id, record_time, flexible, state


async def handle_order(request, ORDERS_PAI_URL):
    """
    Handle a order.
    """

    try:
        ven_id = request.match_info['ven_id']
        data = await request.json()
        device_id, meter_id, resource_id, record_time, flexible, state = parse_order_data(
            data)

        logging.info("=====================================")
        logging.info(f"handle order ven_id: {ven_id}")
        logging.info("=====================================")
        # call tess order api to submit the order
        response_obj = {'status': 'success'}

        tess_order_response = await sumbit_oder_to_oder_api(
            device_id=device_id,
            meter_id=meter_id,
            resource_id=resource_id,
            record_time=record_time,
            flexible=flexible,
            state=state,
            ORDERS_PAI_URL=ORDERS_PAI_URL
        )

        if tess_order_response.status == 200:

            order_id = "123213"
            price = "5.84"
            quantity = "500"
            logging.info("=====================================")
            logging.info(
                f"********* get order_id from TESS succder: {order_id} price:{price}, quantity:{quantity} *********")
            logging.info("send oder_id and price to VEN")
            logging.info("=====================================")
            # send order_id and price to VEN
            if price:
                await send_price_to_ven_through_openadr_event(
                    request=request,
                    ven_id=ven_id,
                    duration=1,
                    timezone=timezone.utc,
                    price=price,
                )
            if quantity and quantity != "0":
                await send_quantity_to_ven_through_openadr_event(
                    request=request,
                    ven_id=ven_id,
                    duration=1,
                    timezone=timezone.utc,
                    quantity=quantity,
                )
            logging.info("trigger event to VEN")

        return web.json_response(response_obj, status=200)

    except Exception as e:
        # Bad path where name is not set

        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)


async def sumbit_oder_to_oder_api(
    device_id: str = None,
    meter_id: str = None,
    resource_id: str = None,
    record_time: str = None,
    flexible: str = None,
    state: str = None,
    ORDERS_PAI_URL: str = None,
):
    """

    """

    dummy_response = {
        "order_id": "!@3123213213",
    }
    await asyncio.sleep(1)
    return web.json_response(dummy_response, status=200)
