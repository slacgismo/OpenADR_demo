

import asyncio

from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS
from models_classes.SharedDeviceInfo import SharedDeviceInfo

from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributeKey

import logging
import time
import logging
import time
from helper.conver_date_to_timestamp import convert_datetime_to_timsestamp, next_market_start_timestamp

from .vtn_api import put_data_to_order_api_of_vtn


async def submit_order_to_vtn(
    vtn_order_url: str = None,
    market_interval: int = 60,
    market_start_time: str = None,
    advanced_seconds: int = 0,
    shared_device_info: SharedDeviceInfo = None,
    # shared_device_info: SharedDeviceInfo = None,
):

    logging.info("Submit order at market start time")

    while True:

        error = shared_device_info.get_error()
        if error:
            # if there is an error from other thread, stop the program
            logging.error(f"====================")
            logging.error(f"critical error: {error}")
            logging.error(f"====================")
            return

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
            device_data = shared_device_info.get_first_item_from_device_data_queue()
            # shared_device_data = SharedDeviceData.get_instance()
            # device_data = shared_device_data.get()
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

            resource_id = shared_device_info.get_resource_id()
            flexible = shared_device_info.get_flexible()
            # state is the USOC value of battery
            state = device_data[SonnenBatteryAttributeKey.USOC.name]
            order_payload = {
                'resource_id': resource_id,
                'flexible': flexible,
                'state': state,
                'record_time': int(time.time()),
            }
            order_id, quantity, price = await put_data_to_order_api_of_vtn(
                order_payload=order_payload,
                vtn_order_url=vtn_order_url
            )
            if order_id is None or quantity is None or price is None:
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
                # clear the device data queue
                shared_device_info.clear_device_data_queue()

        except Exception as e:
            error_message = f"Error submit order: {e}"
            shared_device_info.set_error(error=error_message)
            break
