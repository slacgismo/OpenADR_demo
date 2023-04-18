import asyncio
import logging
from aiohttp import web
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp
from utils.guid import guid
from .handle_event import send_order_id_quantity_price_dispatch_time_ven_through_openadr_event, send_price_to_ven_through_openadr_event
from enum import Enum
from .handle_dispatch import handle_dispatch
import time
import json
from utils.parse_device_id_from_ven_id import parse_device_id_from_ven_id


class ORER_KEYS(Enum):
    ORDER_ID = 'order_id'
    PRICE = 'price'
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'
    AUTION_ID = 'auction_id'


def parse_order_data(data: dict):
    try:
        order_id = data[ORER_KEYS.ORDER_ID.value]
        device_id = data[ORER_KEYS.DEVICE_ID.value]
        resource_id = data[ORER_KEYS.RESOURCE_ID.value]
        flexible = data[ORER_KEYS.FLEXIBLE.value]
        state = data[ORER_KEYS.STATE.value]
        price = data[ORER_KEYS.PRICE.value]
        quantity = data[ORER_KEYS.QUANTITY.value]
        aution_id = data[ORER_KEYS.AUTION_ID.value]
    except Exception as e:
        raise Exception(f"Error parse order data: {e}")
    # state can be None ??
    return order_id, aution_id, device_id, resource_id, flexible, state, price, quantity


async def handle_order(request, ORDERS_API_URL):
    """
    Handle a order.
    return {
        "order_id": order_id,
        'quantity': quantity,
        'price': price,
    }
    """

    try:
        device_id = request.match_info['device_id']
        order_payload = await request.json()

        logging.info("=====================================")
        logging.info(
            f"handle order with device_id:{device_id}")
        logging.info("=====================================")
        # call tess order api to submit the order
        order_body = await sumbit_order_to_order_api(
            device_id=device_id,
            order_payload=order_payload,
            ORDERS_API_URL=ORDERS_API_URL
        )
        # wait till market interval end
        if order_body:
            logging.info(f" order body :{order_body}")

            order_id = order_body.get('order_id')
            price = order_body.get('price')
            quantity = order_body.get('quantity')
            if order_id is None or price is None or quantity is None:
                return web.json_response({"error": "vtn faile to submit order"}, status=400)
            else:
                # send down price to ven by openadr event
                await send_price_to_ven_through_openadr_event(
                    request=request,
                    ven_id=device_id,
                    duration=1,
                    timezone=timezone.utc,
                    price=price,
                )
                payload = {
                    "order_id": order_id,
                    "device_id": device_id,
                    "quantity": quantity,
                    "price": price,
                }
                return web.json_response(payload, status=200)
        else:
            return web.json_response({"error": "vtn faile to submit order"}, status=400)

    except Exception as e:
        raise Exception(f"Error handle order: {e}")


async def sumbit_order_to_order_api(

    device_id: str = None,
    order_payload: dict = None,
    ORDERS_API_URL: str = None,
):
    """
    PUT /order/{device_id}

    response: {
        "order_id": "string",
        'quantity': float,
        'price': float
    }
    """

    order_url = ORDERS_API_URL+f"/{device_id}"
    try:
        logging.info(f"order_url:{order_url}, payload: {order_payload}")
        async with aiohttp.ClientSession() as session:
            async with session.put(order_url, json=order_payload) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    message = await response.text()

                    raise Exception(
                        f"******** Unexpected content type: {content_type} message: {message}")

                if response.status != 200:
                    return None
                    # raise Exception(
                    #     f"Error submit order to TESS: {response.status}")
                else:
                    body = await response.json()
                    return body

    except aiohttp.ClientResponseError as e:
        if e.content_type == 'text/plain':
            raise Exception(f"Error submit order to TESS: {e}\n{await e.text()}")
        else:
            raise Exception(f"Unexpected content type: {e.content_type}")
    except Exception as e:
        raise Exception(f"Error submit order to TESS: {e}")
