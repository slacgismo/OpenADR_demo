

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
from .battery_heursitic_strategy import power_price, power_quantity
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
    is_using_mock_order: bool = False,  # if True, use mock order data
    # shared_device_info: SharedDeviceInfo = None,
):

    logging.info("Submit order at market start time")
    market_index = 0  # this market_index is used to get mapping order dat from mock order data , not used in real order data
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
                is_using_mock_order=is_using_mock_order,
                market_index=market_index,
                market_interval=market_interval
            )

            order_id, dispatch_timestamp, quantity = await put_data_to_order_api_of_vtn(
                device_data=order_data,
                vtn_order_url=vtn_order_url
            )

            # calculate the dispatch timestamp from local here not from TESS.
            # we can also to use local calculated dispatch timestamp to submit order to TESS

            local_calculated_dispatch_timestamp = next_market_start_timestamp(
                market_start_timestamp=market_start_timestamp,
                market_interval=market_interval,
            )
            logging.info("====================================")
            logging.info(
                f"dispatch_timestamp: {dispatch_timestamp} local_calculated_dispatch_timestamp: {local_calculated_dispatch_timestamp}")
            shared_device_info = SharedDeviceInfo.get_instance()
            shared_device_info.set_dispatch_queue(
                dispatch_timestamp=local_calculated_dispatch_timestamp,
                order_id=order_id,
                quantity=quantity
            )

            shared_device_data.clear()
            market_index += 1
        except Exception as e:
            logging.error(f"Error submit order: {e}")
            break


def convert_device_data_to_order_data(
        device_data: dict = None,
        device_type: str = None,
        deivce_brand: str = None,
        is_using_mock_order: bool = False,
        market_index: int = 0,
        simulation_oder_json_file='./actions/dump_orders.json',
        market_interval: int = 60
):
    if device_data is None:
        raise Exception("device_data cannot be None")

    if device_type is None:
        raise Exception("device_type cannot be None")

    shared_device_info = SharedDeviceInfo.get_instance()
    device_id = shared_device_info.get_device_id()
    resource_id = shared_device_info.get_resource_id()
    flexible = shared_device_info.get_flexible()
    # find the recod time
    record_time = None
    state = None
    quantity = None
    price = None
    aution_id = None
    order_id = None

    if is_using_mock_order:
        if not os.path.exists(simulation_oder_json_file):
            raise Exception(
                f"simulation_oder_json_file {simulation_oder_json_file} does not exist")
        logging.info("====================================")
        logging.info("Using mock order data")
        logging.info("====================================")
        # read the mock order data from file
        with open(simulation_oder_json_file, 'r') as f:
            simulation_oder_json = json.load(f)

            if device_id in simulation_oder_json:
                simulation_order_data = simulation_oder_json[device_id]
                index_of_order = market_index % len(simulation_order_data)

                order_id = simulation_order_data[index_of_order][ORER_KEYS.ORDER_ID.value]
                aution_id = simulation_order_data[index_of_order][ORER_KEYS.AUTION_ID.value]
                quantity = simulation_order_data[index_of_order][ORER_KEYS.QUANTITY.value]
                state = simulation_order_data[index_of_order][ORER_KEYS.STATE.value]
                price = simulation_order_data[index_of_order][ORER_KEYS.PRICE.value]

    else:

        if device_type == DEVICE_TYPES.ES.value:
            if deivce_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
                if SonnenBatteryAttributeKey.Timestamp.name in device_data:
                    # TODO: fetch necesary data from TESS API
                    Pmean = 50      # $/MWh auction
                    Pstdev = 5       # $/MWh auction
                    Pmin = 0        # $/MWh resources
                    Pmax = 100      # $/MWh resources
                    Kes = 1     # none  participant
                    Qdesired = 80  # kWh   participant
                    Qmin = 20       # kWh   participant
                    Qmax = 95       # kWh   participant
                    Qcap = 100      # kWh   participant
                    dQmax = 6       # kW    participant
                    # Qlast = last state of USOC
                    Qlast = device_data[SonnenBatteryAttributeKey.USOC.name]
                    # first get the power quantity
                    # quantity = "1000"
                    quantity = power_quantity(
                        Qdesired=Qdesired,
                        Qmin=Qmin,
                        Qmax=Qmax,
                        Qcap=Qcap,
                        Qlast=Qlast,
                        dQmax=dQmax,
                    )
                    # Second get the price
                    price = power_price(
                        Pmean=Pmean,
                        Pstdev=Pstdev,
                        Pmin=Pmin,
                        Pmax=Pmax,
                        Qlast=Qlast,
                        Qdesired=Qdesired,
                        Qmin=Qmin,
                        Qmax=Qmax,
                        Kes=Kes,

                    )

                    logging.warning(
                        f"-----------  quantity  {quantity} W, price is {price} -----------")
                    state = device_data[SonnenBatteryAttributeKey.Pac_total_W.name]
                    # price = "1.2"
                    # ? should we generated aution_id here?
                    aution_id = str(guid())
                    order_id = str(guid())
                else:
                    raise Exception("timestamp is not in device_data")
            else:
                raise Exception(
                    "device_brand is not supported, please implement it")

    order_data = {
        ORER_KEYS.ORDER_ID.value: order_id,
        ORER_KEYS.DEVICE_ID.value: device_id,
        ORER_KEYS.RESOURCE_ID.value: resource_id,
        ORER_KEYS.RECORD_TIME.value: record_time,
        ORER_KEYS.FLEXIBLE.value: flexible,
        ORER_KEYS.STATE.value: state,
        ORER_KEYS.QUANTITY.value: quantity,
        ORER_KEYS.PRICE.value: price,
        ORER_KEYS.AUTION_ID.value: aution_id
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
                if response.status != 200:
                    # TODO: handle 400, 401, 403, 404, 500
                    raise Exception(
                        f"Submit order to Order API response status code: {response.status}")
                else:
                    body = await response.json()
                    logging.info(
                        f"************ Submit to VTN Order API response body: {body} ************")
                    # for key in body:
                    #     logging.info(f"key: {key}, value: {body[key]}")
                    order_id = body['order_id']
                    dispatch_timestamp = body['dispatch_timestamp']
                    quantity = body['quantity']
                    return order_id, dispatch_timestamp, quantity
    except Exception as e:
        logging.error(f"Error submit order to Order API: {e}")
        raise Exception(f"Error checking Order API: {e}")
