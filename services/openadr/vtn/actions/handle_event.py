import asyncio
import logging
from aiohttp import web
import datetime
from datetime import datetime, timezone, timedelta
import aiohttp
from utils.guid import guid
from openleadr.enums import SIGNAL_NAME, SIGNAL_TYPE
import json


async def send_price_to_ven_through_openadr_event(request,
                                                  ven_id,
                                                  duration,
                                                  timezone,
                                                  price: float
                                                  ):
    server = request.app["server"]
    server.add_event(ven_id=ven_id,
                     signal_name="BID_PRICE",
                     signal_type="price",
                     intervals=[{'dtstart': datetime.now(timezone.utc),
                                 'duration': timedelta(minutes=int(duration)),
                                 'signal_payload': price}],
                     callback=price_event_response_callback,
                     event_id=str(guid()),
                     )
    logging.info(f"send price: {price} to VEN: {ven_id}")


async def price_event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    logging.info(
        f"VEN: {ven_id} responded to Event {event_id} with: {opt_type}")


async def send_quantity_to_ven_through_openadr_event(request,
                                                     ven_id,
                                                     duration,
                                                     timezone,
                                                     quantity: float
                                                     ):
    server = request.app["server"]
    server.add_event(ven_id=ven_id,
                     signal_name="LOAD_DISPATCH",
                     signal_type='level',
                     intervals=[{'dtstart': datetime.now(timezone.utc),
                                 'duration': timedelta(minutes=int(duration)),
                                 'signal_payload': quantity}],
                     callback=quantity_event_response_callback,
                     event_id=str(guid()),
                     )
    logging.info(f"send quantity: {quantity} to VEN: {ven_id}")


async def quantity_event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    logging.info(
        f"VEN: {ven_id} responded to Event {event_id} with: {opt_type}")


async def send_order_id_quantity_price_dispatch_time_ven_through_openadr_event(request,
                                                                               ven_id,
                                                                               duration,
                                                                               timezone,
                                                                               order_id: str,
                                                                               quantity: float,
                                                                               price: float,
                                                                               dispatch_timestamp: int
                                                                               ):
    payload = {
        "oder_id": order_id,
        "quantity": quantity,
        "price": price,
        "dispatch_timestamp": dispatch_timestamp

    }

    server = request.app["server"]
    server.add_event(ven_id=ven_id,
                     signal_name="LOAD_DISPATCH",
                     signal_type='level',
                     intervals=[{'dtstart': datetime.now(timezone.utc),
                                 'duration': timedelta(minutes=int(duration)),
                                 'signal_payload': json.dumps(payload)}],
                     callback=order_id_event_call_back,
                     event_id=str(guid()),
                     )
    logging.info("===============================================")
    logging.info(f"send payload: {payload} to VEN: {ven_id}")


async def order_id_event_call_back(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    logging.info(
        f"VEN: {ven_id} responded to Event {event_id} with: {opt_type}")
