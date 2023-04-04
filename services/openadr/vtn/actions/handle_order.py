import asyncio
import logging
from aiohttp import web
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp
from utils.guid import guid
from .handle_event import send_price_to_ven_through_openadr_event, send_quantity_to_ven_through_openadr_event
from enum import Enum
from .handle_dispatch import handle_dispatch


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


async def handle_order(request, ORDERS_PAI_URL, DISPATCHES_API_URL):
    """
    Handle a order.
    """

    try:
        ven_id = request.match_info['ven_id']
        data = await request.json()
        device_id, meter_id, resource_id, record_time, flexible, state = parse_order_data(
            data)

        logging.info("=====================================")
        logging.info(f"handle order ven_id: {ven_id} device_id:{device_id}")
        logging.info("=====================================")
        # call tess order api to submit the order
        response_obj = {'status': 'success'}
        quantity = "1000"
        tess_order_response = await sumbit_oder_to_oder_api(
            device_id=device_id,
            resource_id=resource_id,
            quantity=quantity,
            record_time=record_time,
            flexible=flexible,
            state=state,
            ORDERS_PAI_URL=ORDERS_PAI_URL
        )

        if tess_order_response.status == 200:

            body = await tess_order_response.json()
            if 'order_id' not in body or 'price' not in body:
                raise Exception(
                    f"Error parse order data: {tess_order_response}")

            order_id = body['order_id']
            price = body['price']
            if price:
                await send_price_to_ven_through_openadr_event(
                    request=request,
                    ven_id=ven_id,
                    duration=1,
                    timezone=timezone.utc,
                    price=price,
                )
            # wait for the dispatch response and send quantity to VEN
            dispatch_response = await handle_dispatch(
                order_id=order_id,
                DISPATCHES_API_URL=DISPATCHES_API_URL)

            # ask the quantity and price from TESS dispatch
            if dispatch_response.status == 200:
                dispatch_body = await dispatch_response.json()
                if 'quantity' not in dispatch_body:
                    raise Exception(
                        f"Error parse dispatch data: {dispatch_body}")

                quantity = dispatch_body['quantity']

                logging.info(f"Get quantity and price from dispatch success")

                if quantity:
                    await send_quantity_to_ven_through_openadr_event(
                        request=request,
                        ven_id=ven_id,
                        duration=1,
                        timezone=timezone.utc,
                        quantity=quantity,
                    )
            else:
                logging.error(
                    f"dispatch failed {dispatch_response.status} {dispatch_response}")

            logging.info("trigger event to VEN")
            response_obj = {'status': 'success', 'info': "submit oder success"}
            return web.json_response(response_obj, status=200)
        else:

            logging.info("=====================================")
            response_obj = {'status': 'failed', 'info': tess_order_response}
            return web.json_response(response_obj, status=500)
            # return failed with a status code of 500 i.e. 'Server Error'

    except Exception as e:
        # Bad path where name is not set
        logging.error(f"Submit order to TESS failed {e}")
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)


async def sumbit_oder_to_oder_api(
    device_id: str = None,
    resource_id: str = None,
    record_time: str = None,
    quantity: str = None,
    flexible: str = None,
    state: str = None,
    ORDERS_PAI_URL: str = None,
):
    """
    PUT /order/{device_id}
    """

    data = {
        'resource_id': resource_id,
        'quantity': quantity,
        'record_time': record_time,
        'flexible': flexible,
        'state': state
    }
    order_url = ORDERS_PAI_URL+f"/{device_id}"
    try:

        async with aiohttp.ClientSession() as session:
            async with session.put(order_url, json=data) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    raise Exception(f"Unexpected content type: {content_type}")
                body = await response.json()
                return response

    except Exception as e:
        raise Exception(f"Error submit order to TESS: {e}")
