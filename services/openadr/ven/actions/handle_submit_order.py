

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
from helper.conver_date_to_timestamp import wait_till_next_market_start_time, current_market_start_timestamp, convert_datetime_to_timsestamp
from models_classes.SharedDeviceData import SharedDeviceData
import aiohttp
from enum import Enum


class ORER_KEYS(Enum):
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    METER_ID = 'meter_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'


async def submit_order_to_vtn(
    vtn_order_url: str = None,
    market_interval: int = 60,
    market_start_time: str = None,
    advanced_seconds: int = 0,
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
                logging.info("No device data to submit measurement")
                logging.info("====================================")
            else:
                order_data = convert_device_data_to_order_data(
                    device_data=device_data,
                    device_type=DEVICE_TYPES.ES.value,
                    deivce_brand=BATTERY_BRANDS.SONNEN_BATTERY.value
                )

                await put_data_to_order_api_of_vtn(
                    device_data=order_data,
                    vtn_order_url=vtn_order_url
                )

        except Exception as e:
            logging.error(f"Error submit order: {e}")
            break


def convert_device_data_to_order_data(device_data: dict = None, device_type: str = None, deivce_brand: str = None):
    if device_data is None:
        raise Exception("device_data cannot be None")

    if device_type is None:
        raise Exception("device_type cannot be None")
    # find the recod time
    record_time = None
    state = None
    quantity = None
    if device_type == DEVICE_TYPES.ES.value:
        if deivce_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
            if SonnenBatteryAttributeKey.Timestamp.name in device_data:
                record_time = device_data[SonnenBatteryAttributeKey.Timestamp.name]
                quantity = "1000"
                logging.warning(
                    "----------- TODO: quantity is hard coded 1000 W-----------")
                state = device_data[SonnenBatteryAttributeKey.Pac_total_W.name]
            else:
                raise Exception("timestamp is not in device_data")
        else:
            raise Exception(
                "device_brand is not supported, please implement it")

    shared_device_info = SharedDeviceInfo.get_instance()
    device_id = shared_device_info.get_device_id()
    resource_id = shared_device_info.get_resource_id()
    meter_id = shared_device_info.get_meter_id()
    flexible = shared_device_info.get_flexible()

    order_data = {
        ORER_KEYS.DEVICE_ID.value: device_id,
        ORER_KEYS.METER_ID.value: meter_id,
        ORER_KEYS.RESOURCE_ID.value: resource_id,
        ORER_KEYS.RECORD_TIME.value: record_time,
        ORER_KEYS.FLEXIBLE.value: flexible,
        ORER_KEYS.STATE.value: state,
        ORER_KEYS.QUANTITY.value: quantity
    }

    return order_data


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
                response_text = await response.text()
                logging.info(
                    f"Submit order to Order API response: {response_text}")
                if response.status != 200:
                    # TODO: handle 400, 401, 403, 404, 500
                    raise Exception(
                        f"Submit order to Order API response status code: {response.status}")
                else:
                    logging.info(
                        f"************ Submit to VTN Order API response: success ************")
    except Exception as e:
        raise Exception(f"Error checking Order API: {e}")
    return response_text
