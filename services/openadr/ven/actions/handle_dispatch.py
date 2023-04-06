
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import logging
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributeKey
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
import time
import asyncio
import aiohttp
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
import json
from helper.guid import guid
import os


async def submit_dispatch_to_vtn(
    vtn_dispatch_url: str = None,
    order_id: str = None,
    timeout: int = 10,
):
    url = vtn_dispatch_url
    dispatch_data = {
        "order_id": order_id,
    }
    logging.info(
        f"send dispatch request to TESS dispatch api: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.put(vtn_dispatch_url, json=dispatch_data, timeout=timeout) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                text = await response.text()
                logging.error(
                    f"Unexpected content type: {content_type} {text}")
                raise Exception(f"Unexpected content type: {content_type}")
            if response.status != 200:
                raise Exception(
                    f"Error submit order to TESS: {response.status}")
            return await response.json()


# async def handle_dispatch(
#     vtn_dispatch_url: str = None,
#     shared_device_info: SharedDeviceInfo = None,
#     market_start_time: str = None,
#     advanced_seconds: int = 0,
#     market_interval: str = None
# ):
    # while True:
    #     try:
    #         print("handle_dispatch start")
    #         market_start_timestamp = convert_datetime_to_timsestamp(
    #             time_str=market_start_time)
    #         # get the current time
    #         current_time = int(time.time())
    #         time_since_start = current_time - \
    #             (market_start_timestamp - advanced_seconds)
    #         time_to_next_start = market_interval - \
    #             (time_since_start % market_interval)
    #         # calculate the next marekt start timestamp

    #         while time_to_next_start > 0:
    #             await asyncio.sleep(1)
    #             if time_to_next_start % 1 == 0:
    #                 logging.info(
    #                     f"Waiting for next market start time, {time_to_next_start} seconds left")
    #             time_to_next_start -= 1
    #         order_id = "d2d07b7aa447099acb3a7990e3af82"
    #         response_message = await submit_dispatch_to_vtn(
    #             vtn_dispatch_url=vtn_dispatch_url,
    #             order_id=order_id,

    #         )
    #     except Exception as e:
    #         logging.error(f"Error in dispatch loop: {e}")
    #         raise Exception(f"Error in dispatch loop: {e}")


async def handle_dispatch(
    vtn_dispatch_url: str = None,
    shared_device_info: SharedDeviceInfo = None,
):
    logging.info("========================================")
    logging.info("Start dispatch loop")
    logging.info("========================================")
    ven_id = shared_device_info.get_ven_id()
    while True:
        try:
            dispatch_info = shared_device_info.get_first_dispatch()
            if dispatch_info is None:
                # logging.info("No dispatch request")
                await asyncio.sleep(1)
            else:
                logging.error("========================================")
                logging.info("Invoek dispatch request")
                length_of_queue = shared_device_info.len_dispatch_queue()
                dispatch_timestamp = dispatch_info['dispatch_timestamp']
                order_id = dispatch_info['order_id']
                quantity = dispatch_info['quantity']
                current_time = int(time.time())
                market_interval = shared_device_info.get_market_interval()
                time_to_wait = dispatch_timestamp - current_time
                if time_to_wait > market_interval:
                    raise Exception(
                        f"Time to wait dispathch: {time_to_wait} is greater than market interval")
                while time_to_wait > 0:
                    await asyncio.sleep(1)
                    if time_to_wait % 2 == 0:
                        logging.info(
                            f"Waiting for dispatch...{time_to_wait}")
                    time_to_wait -= 1
                logging.info(
                    f"Reach dispatch time at {int(time.time())}, dispatch_timestapm : {dispatch_timestamp}.")

                response_message = await submit_dispatch_to_vtn(
                    vtn_dispatch_url=vtn_dispatch_url,
                    order_id=order_id,

                )
                if 'quantity' not in response_message:
                    raise Exception(
                        f"Dispatch response does not contain quantity: {response_message}")
                quantity = response_message['quantity']
                logging.info(f"Dispatch response: {response_message}")
                await send_dispatch_quantity_to_device(
                    device_settings=shared_device_info.get_device_settings(),
                    device_type=shared_device_info.get_device_type(),
                    dispatch_quantity=float(quantity),
                    is_using_mock_device=shared_device_info.get_is_using_mock_device(),
                    emulated_device_api_url=shared_device_info.get_emulated_device_api_url(),
                    # enable_self_consumption is to prevent battery fully discharge. Setup to Truen when finish test, this is for test purpose only. Always set to False in production.
                    enable_self_consumption=False,

                )
        except Exception as e:
            logging.error("========================================")
            logging.error(f"Error in dispatch loop: {e}")
            logging.error("========================================")
            raise Exception(f"Error in dispatch loop: {e}")


async def send_dispatch_quantity_to_device(
    device_settings: dict = None,
    device_type: str = None,
    dispatch_quantity: float = None,
    is_using_mock_device: bool = False,
    emulated_device_api_url: str = None,
    enable_self_consumption: bool = False,
):
    """
    Handle a dispatch request.
    enable_self_consumption is for test only. Always set to False in production.
    However, when you done with battery test, you have to set it to True to prevent the battery from fully discharging.
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
                else:
                    # logging.info(
                    #     f"device_settings {key} is unknown: {device_settings}")
                    raise Exception(
                        f"device_settings {key} is unknown: {device_settings}")

        except Exception as e:
            # logging.error(
            #     f"Error parsing device settings: {device_settings}, error: {e}")
            raise Exception(
                f"Error parsing device settings: {device_settings}, error: {e}")

        try:
            if device_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
                batter_data = dict()
                if is_using_mock_device:
                    logging.info(
                        "=========  Send dispatch to Mock battery  ==================")
                    mock_battery_interface = MockSonnenInterface(
                        serial=battery_sn, auth_token=battery_token, url_ini=emulated_device_api_url)
                    # get battery data from device
                    response = await mock_battery_interface.enable_manual_mode()
                    if response['status'] == "0":
                        if dispatch_quantity < 0:
                            mode = 'discharge'
                        else:
                            mode = 'charge'
                        manul_mode_control_response = await mock_battery_interface.manual_mode_control(
                            mode=mode, value=str(abs(dispatch_quantity)))  # remmeber to use absouute value since we already check the mode
                        logging.info(
                            f"manul_mode_control_response : {manul_mode_control_response}")
                        if 'ReturnCode' in manul_mode_control_response:
                            if manul_mode_control_response['ReturnCode'] == "0":
                                logging.info(
                                    "manual_mode_control success")
                            else:
                                raise Exception(
                                    f"manual_mode_control failed: {manul_mode_control_response}")
                else:

                    logging.info(
                        "======== Send dispatch to real battery ==================")
                    battery_interface = SonnenInterface(
                        serial=battery_sn, auth_token=battery_token)
                    # get battery data from device
                    # batter_data = await battery_interface.get_status()
                    if enable_self_consumption is True:
                        enable_self_consumption_response = await battery_interface.enable_self_consumption()
                        logging.info(
                            f"enable_self_consumption_response:{enable_self_consumption_response}")
                        if enable_self_consumption_response['status'] == "0":
                            logging.info(
                                "enable_self_consumption success")
                        else:
                            raise Exception(
                                f"enable_self_consumption failed: {enable_self_consumption_response}")
                        return

                    # enable manual mode
                    response = await battery_interface.enable_manual_mode()
                    logging.info(
                        f"enable_manual_mode response: {response}")
                    if response['status'] == "0":
                        if dispatch_quantity < 0:
                            mode = 'discharge'
                        else:
                            mode = 'charge'

                        logging.info(
                            "enable_manual_mode success")
                        manul_mode_control_response = await battery_interface.manual_mode_control(
                            mode=mode, value=str(abs(dispatch_quantity)))  # remmeber to use absouute value since we already check the mode
                        logging.info(
                            f"manul_mode_control_response : {manul_mode_control_response}")
                        if 'ReturnCode' in manul_mode_control_response:
                            if manul_mode_control_response['ReturnCode'] == "0":
                                logging.info(
                                    "manual_mode_control success")
                            else:
                                raise Exception(
                                    f"manual_mode_control failed: {manul_mode_control_response}")
                        logging.warning(
                            "TODO:After the test. Please always enable_self_consumption() to prvent battery from fully discharging"
                        )

                    else:
                        raise Exception(
                            f"enable_manual_mode failed: {response}")

            else:
                raise Exception(
                    f"Device brand {device_brand} is not supported yet")
        except Exception as e:
            raise Exception(f"Error getting battery data from API: {e}")
    else:
        raise Exception(f"Device type {device_type} is not supported yet")

    # order_id = response_message['order_id']
    # dispatch_quantity = response_message['quantity']
    # submit dispatch to vtn

    # async def handle_dispatch(
    #     dispatch_timestamp: int = None,
    #     market_interval: int = None,
    #     dispatch_quantity: float = None,
    #     # device_settings: dict = None,
    #     # device_type: str = None,
    #     # is_using_mock_device: bool = False,
    #     # emulated_device_api_url: str = None,
    #     # # this is for test only # always set to False in production, However, i
    #     # enable_self_consumption: bool = False,
    #     vtn_dispatch_url: str = None,
    #     order_id: str = None,
    # ):
    #     """
    #     Handle a dispatch request.
    #     enable_self_consumption is for test only. Always set to False in production.
    #     However, when you done with battery test, you have to set it to True to prevent the battery from fully discharging.
    #     """

    #     current_time = int(time.time())
    #     time_to_wait = dispatch_timestamp - current_time
    #     if time_to_wait > market_interval:
    #         raise Exception(
    #             f"Time to wait dispathch: {time_to_wait} is greater than market interval")

    #     while time_to_wait > 0:
    #         await asyncio.sleep(1)
    #         if time_to_wait % 2 == 0:
    #             logging.info("Waiting for dispatch...")
    #         time_to_wait -= 1

    #     # end of waiting for dispatch
    #     # send the dispatch request to the device
    #     dispatch_body = await submit_dispatch_to_VTN(
    #         vtn_dispatch_url=vtn_dispatch_url,
    #         order_id=order_id,
    #     )
    #     logging.info(f"Dispatch request sent to VTN {dispatch_body}")

    # if dispatch_quantity is None:
    #     raise Exception("dispatch_quantity is None")

    # if device_type == DEVICE_TYPES.ES.value:
    #     try:
    #         for key, value in device_settings.items():

    #             if value is None:
    #                 # logging.error("value is None")
    #                 raise Exception(
    #                     f"device_settings {key} is None: {device_settings}")
    #             if key == SONNEN_BATTERY_DEVICE_SETTINGS.DEVICE_BRAND.value:
    #                 device_brand = value
    #             elif key == SONNEN_BATTERY_DEVICE_SETTINGS.BATTERY_SN.value:
    #                 battery_sn = value
    #             elif key == SONNEN_BATTERY_DEVICE_SETTINGS.BATTERY_TOKEN.value:
    #                 battery_token = value
    #             else:
    #                 # logging.info(
    #                 #     f"device_settings {key} is unknown: {device_settings}")
    #                 raise Exception(
    #                     f"device_settings {key} is unknown: {device_settings}")

    #     except Exception as e:
    #         # logging.error(
    #         #     f"Error parsing device settings: {device_settings}, error: {e}")
    #         raise Exception(
    #             f"Error parsing device settings: {device_settings}, error: {e}")

    #     try:
    #         if device_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
    #             batter_data = dict()
    #             if is_using_mock_device:
    #                 logging.info(
    #                     "=========  Send dispatch to Mock battery  ==================")
    #                 mock_battery_interface = MockSonnenInterface(
    #                     serial=battery_sn, auth_token=battery_token, url_ini=emulated_device_api_url)
    #                 #
    #             else:
    #                 logging.info(
    #                     "======== Send dispatch to real battery ==================")
    #                 battery_interface = SonnenInterface(
    #                     serial=battery_sn, auth_token=battery_token)
    #                 # get battery data from device
    #                 # batter_data = await battery_interface.get_status()
    #                 if enable_self_consumption is True:
    #                     enable_self_consumption_response = await battery_interface.enable_self_consumption()
    #                     logging.info(
    #                         f"enable_self_consumption_response:{enable_self_consumption_response}")
    #                     if enable_self_consumption_response['status'] == "0":
    #                         logging.info(
    #                             "enable_self_consumption success")
    #                     else:
    #                         raise Exception(
    #                             f"enable_self_consumption failed: {enable_self_consumption_response}")
    #                     return

    #                 # enable manual mode
    #                 response = await battery_interface.enable_manual_mode()
    #                 logging.info(f"enable_manual_mode response: {response}")
    #                 if response['status'] == "0":
    #                     if dispatch_quantity < 0:
    #                         mode = 'discharge'
    #                     else:
    #                         mode = 'charge'

    #                     logging.info(
    #                         "enable_manual_mode success")
    #                     manul_mode_control_response = await battery_interface.manual_mode_control(
    #                         mode=mode, value=str(abs(dispatch_quantity)))  # remmeber to use absouute value since we already check the mode
    #                     logging.info(
    #                         f"manul_mode_control_response : {manul_mode_control_response}")
    #                     if 'ReturnCode' in manul_mode_control_response:
    #                         if manul_mode_control_response['ReturnCode'] == "0":
    #                             logging.info(
    #                                 "manual_mode_control success")
    #                         else:
    #                             raise Exception(
    #                                 f"manual_mode_control failed: {manul_mode_control_response}")
    #                     logging.warning(
    #                         "TODO:After the test. Please always enable_self_consumption() to prvent battery from fully discharging"
    #                     )

    #                 else:
    #                     raise Exception(
    #                         f"enable_manual_mode failed: {response}")

    #         else:
    #             raise Exception(
    #                 f"Device brand {device_brand} is not supported yet")
    #     except Exception as e:
    #         raise Exception(f"Error getting battery data from API: {e}")
    # else:
    #     raise Exception(f"Device type {device_type} is not supported yet")

    # async def submit_dispatch_to_VTN(
    #     vtn_dispatch_url: str = None,
    #     order_id: str = None,
    # ):
    #     """
    #     Submit the dispatch request to the VTN
    #     """
    #     if vtn_dispatch_url is None:
    #         raise Exception("vtn_dispatch_url is None")
    #     if order_id is None:
    #         raise Exception("order_id is None")
    #     try:
    #         payload = {
    #             "order_id": order_id,
    #         }
    #         async with aiohttp.ClientSession() as session:
    #             async with session.put(vtn_dispatch_url, json=payload) as response:
    #                 response_text = await response.text()
    #                 logging.info(
    #                     f"Submit order to Order API response: {response_text}")
    #                 if response.status != 200:
    #                     # TODO: handle 400, 401, 403, 404, 500
    #                     raise Exception(
    #                         f"Submit order to Order API response status code: {response.status}")
    #                 else:
    #                     body = await response.json()
    #                     logging.info(
    #                         f"************ Submit to VTN Order API response body: {body} ************")
    #                     return body
    #     except Exception as e:
    #         raise Exception(f"Error checking Order API: {e}")
