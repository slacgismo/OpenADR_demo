

from api.sonnen_battery.filter_battery_data import filter_battery_data
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
from models_classes.Constants import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from typing import Dict
import logging
import time
import logging
import time
from helper.conver_date_to_timestamp import wait_till_next_market_start_time

import aiohttp
from enum import Enum
import json
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributes, SonnenBatterySystemStatus
from models_classes.SharedDeviceInfo import SharedDeviceInfo
from .vtn_api import put_data_to_meter_api


async def handle_get_device_data(
    market_interval: int = 60,
    device_brand: str = None,
    device_id: str = None,
    meter_id: str = None,
    resource_id: str = None,
    market_start_time: str = None,
    is_using_mock_device: bool = False,
    device_type: str = None,
    emulated_device_api_url: str = None,
    device_settings: dict = None,
    advanced_seconds_of_market_startime: int = 0,
    vtn_measurement_url: str = None,
    shared_device_info: SharedDeviceInfo = None,
):
    logging.info(
        f"Get device before {advanced_seconds_of_market_startime} market start time")
    while True:
        error = shared_device_info.get_error()
        if error:
            # if there is an error from other thread, stop the program
            logging.error(f"====================")
            logging.error(f"critical error: {error}")
            logging.error(f"====================")
            return

        await wait_till_next_market_start_time(
            market_start_time=market_start_time,
            market_interval=market_interval,
            advanced_seconds_of_market_startime=advanced_seconds_of_market_startime,
            funciton_name="get_device_data"
        )
        current_time = int(time.time())

        logging.info(
            "-------------- get device data ----------------------")
        logging.info(
            f"start to get device data at {current_time} ")
        logging.info("------------------------------------")
        try:
            device_data = await get_devices_data(
                is_using_mock_device=is_using_mock_device,
                device_type=device_type,
                emulated_device_api_url=emulated_device_api_url,
                device_settings=device_settings
            )
            # save the device data to the shared memory for other thread to use
            # logging.info(f"device_data: {device_data}")

            # save device data to a queue
            # always clear the queue before put new data
            shared_device_info.clear_device_data_queue()
            shared_device_info.append_device_data_queue(device_data)

            # shared_device_data = SharedDeviceData.get_instance()
            # shared_device_data.set(device_data)
            logging.warning(f"put data to meter api need to be verified")

            status = device_data[SonnenBatteryAttributes.SystemStatus.name]
            if status == SonnenBatterySystemStatus.OnGrid.name:
                status = "1"
            elif status == SonnenBatterySystemStatus.OffGrid.name:
                status = "0"
            else:
                raise Exception(f"status {status} is not supported yet")

            timestamp = device_data[SonnenBatteryAttributes.Timestamp.name]

            is_submit_data_to_vtn_success = put_data_to_meter_api(
                readings=json.dumps(device_data),
                device_id=device_id,
                meter_id=meter_id,
                resource_id=resource_id,
                device_brand=device_brand,
                status=status,
                timestamp=timestamp,
                vtn_measurement_url=vtn_measurement_url)

            if is_submit_data_to_vtn_success is False:
                raise Exception(f"Error put data to vtn meter")

        except Exception as e:
            error_message = f"Error get device data: {e}"
            shared_device_info.set_error(error=error_message)
            break
            # logging.error(f"Error get device data {e}")
            # raise Exception(f"Error get device data: {e}")


async def get_devices_data(
    device_type: str = None,
    is_using_mock_device: bool = False,
    device_settings: dict = None,
    emulated_device_api_url: str = None,
) -> Dict:
    """
    Get devices data.
    """

    if device_type == DEVICE_TYPES.ES.value:
        try:
            for key, value in device_settings.items():

                if value is None:
                    # logging.error("value is None")
                    raise Exception(
                        f"device_settings {key} is None: {device_settings}")
                if key == SONNEN_BATTERY_DEVICE_SETTINGS.DEVICE_BRAND.value:
                    device_brand = value
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.BATTERY_SN.value:
                    battery_sn = value
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.BATTERY_TOKEN.value:
                    battery_token = value
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.FLEXIBLE.value:
                    pass
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.IS_USING_MOCK_DEVICE.value:
                    pass
                else:
                    raise Exception(
                        f"device_settings {key} is unknown: {device_settings}")

        except Exception as e:

            raise Exception(
                f"Error parsing device settings: {device_settings}, error: {e}")
        try:
            if device_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
                filter_data = await get_sonnen_battery_data(
                    is_using_mock_device=is_using_mock_device,
                    battery_sn=battery_sn,
                    battery_token=battery_token,
                    emulated_device_api_url=emulated_device_api_url,
                    device_brand=device_brand
                )
                return filter_data
            else:
                raise Exception(
                    f"Device brand {device_brand} is not supported yet")
        except Exception as e:
            raise Exception(f"Error getting battery data from API: {e}")
    else:
        raise Exception(f"Device type {device_type} is not supported yet")


async def get_sonnen_battery_data(
        is_using_mock_device: bool = False,
        battery_sn: str = None,
        battery_token: str = None,
        device_brand: str = None,
        emulated_device_api_url: str = None):
    if is_using_mock_device:
        logging.info(
            "=========  GET Mock battery data ==================")
        mock_battery_interface = MockSonnenInterface(
            serial=battery_sn, auth_token=battery_token, url_ini=emulated_device_api_url, device_brand=device_brand)
        # get battery data from mock device
        batter_data = await mock_battery_interface.get_mock_battery_status()
        filter_data = await filter_battery_data(batter_data)
        logging.info(
            f"=========  length of filter_data {len(filter_data)} ==================")
        return filter_data
    else:
        logging.info(
            "======== GET real battery data ==================")
        battery_interface = SonnenInterface(
            serial=battery_sn, auth_token=battery_token)
        # get battery data from device
        batter_data = await battery_interface.get_status()

    if batter_data is None:
        raise Exception(
            f"batter_data is None: {batter_data}")
    else:
        filter_data = await filter_battery_data(batter_data)
        # logging.info(filter_data)
        return filter_data
