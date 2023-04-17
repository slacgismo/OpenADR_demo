

import asyncio
from api.sonnen_battery.filter_battery_data import filter_battery_data
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from models_classes.SharedDeviceInfo import SharedDeviceInfo
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributeKey
from typing import Dict
import logging
import time
import logging
import time
from helper.conver_date_to_timestamp import wait_till_next_market_start_time, current_market_start_timestamp, convert_datetime_to_timsestamp, next_market_start_timestamp
from models_classes.SharedDeviceData import SharedDeviceData
import aiohttp
from enum import Enum
import json
from helper.guid import guid
import os
from .handle_dispatch import handle_dispatch
from .battery_heursitic_strategy import convert_device_data_to_order_data
import random


class ORER_KEYS(Enum):
    ORDER_ID = 'order_id'
    PRICE = 'price'
    AUTION_ID = 'auction_id'
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'


async def submit_order_to_vtn(
    vtn_order_url: str = None,
    market_interval: int = 60,
    market_start_time: str = None,
    advanced_seconds: int = 0,
    price_floor: float = None,
    price_ceiling: float = None
    # shared_device_info: SharedDeviceInfo = None,
):

    logging.info("Submit order at market start time")

    while True:
        market_start_timestamp = convert_datetime_to_timsestamp(
            time_str=market_start_time)
        # get the current time
        current_time = int(time.time())
        time_since_start = current_time - \
            (market_start_timestamp - advanced_seconds)
        time_to_next_start = market_interval - \
            (time_since_start % market_interval)
        # calculate the next marekt start timestamp

        while time_to_next_start > 0:
            await asyncio.sleep(1)
            if time_to_next_start % 10 == 0:
                logging.info(
                    f"Waiting for next market start time, {time_to_next_start} seconds left")
            time_to_next_start -= 1

        current_time = int(time.time())
        logging.info("============== order ===============")
        logging.info(
            f"start to submit order data at {current_time}")
        logging.info("====================================")

        try:

            shared_device_data = SharedDeviceData.get_instance()
            device_data = shared_device_data.get()

            if device_data is None:
                logging.info("====================================")
                logging.info(
                    f" :No device data to submit order, skip this market interval")
                logging.info("====================================")
                continue

            # check the Uac value, if it is 0, skip this market interval
            Uac = device_data[SonnenBatteryAttributeKey.Uac.name]
            if Uac == 0:
                logging.info("====================================")
                logging.info(
                    "Uac is 0, battery is offgrid, skip this market interval")
                logging.info("====================================")
                continue

            order_data = convert_device_data_to_order_data(
                device_data=device_data,
                device_type=DEVICE_TYPES.ES.value,
                deivce_brand=BATTERY_BRANDS.SONNEN_BATTERY.value,

                market_interval=market_interval,
                price_floor=price_floor,
                price_ceiling=price_ceiling
            )

            order_id, quantity = await put_data_to_order_api_of_vtn(
                device_data=order_data,
                vtn_order_url=vtn_order_url
            )
            if order_id is None or quantity is None:
                logging.warning(
                    "Error submit order, order_id or quantity is None, skip this market interval. clear dispatch queue")
                shared_device_info = SharedDeviceInfo.get_instance()
                shared_device_info.clear_dispatch_queue()
            else:
                # calculate the dispatch timestamp from local here not from TESS.
                # we can also to use local calculated dispatch timestamp to submit order to TESS
                local_calculated_dispatch_timestamp = next_market_start_timestamp(
                    market_start_timestamp=market_start_timestamp,
                    market_interval=market_interval,
                )
                logging.info("====================================")
                logging.info(
                    f" local_calculated_dispatch_timestamp: {local_calculated_dispatch_timestamp}")
                shared_device_info = SharedDeviceInfo.get_instance()
                shared_device_info.set_dispatch_queue(
                    dispatch_timestamp=local_calculated_dispatch_timestamp,
                    order_id=order_id,
                    quantity=quantity
                )

                shared_device_data.clear()
        except Exception as e:
            logging.error(f"Error submit order: {e}")
            break


async def put_data_to_order_api_of_vtn(
    device_data: dict = None,
    vtn_order_url: str = None,
):
    if device_data is None or vtn_order_url is None:
        raise Exception(
            "data, vtn order cannot be None")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(vtn_order_url, json=device_data) as response:
                if response.status != 200:
                    # TODO: handle 400, 401, 403, 404, 500
                    logging.error(
                        f"-------- VEN Submit order to Order API response status code: {response.status} --------")
                    return None, None
                    # raise Exception(
                    #     f"-------- Submit order to Order API response status code: {response.status} --------")
                else:
                    body = await response.json()
                    logging.info(
                        f"************ Submit to VTN Order API response body: {body} ************")
                    # for key in body:
                    #     logging.info(f"key: {key}, value: {body[key]}")
                    order_id = body['order_id']
                    # dispatch_timestamp = body['dispatch_timestamp']
                    quantity = body['quantity']
                    return order_id, quantity
    except Exception as e:
        logging.error(f"Error submit order to Order API: {e}")
        raise Exception(f"Error checking Order API: {e}")
