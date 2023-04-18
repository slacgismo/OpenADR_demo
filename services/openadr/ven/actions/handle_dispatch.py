
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import logging

import time
import asyncio
import aiohttp
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from models_classes.SharedDeviceInfo import SharedDeviceInfo
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
import logging
import time
import logging
import time
import aiohttp
from .vtn_api import submit_dispatch_to_vtn
from .control_devices import send_dispatch_quantity_to_devices


async def handle_dispatch(
    vtn_dispatch_url: str = None,
    shared_device_info: SharedDeviceInfo = None,
    # enable_self_consumption is to prevent battery fully discharge. Setup to Truen when finish test, this is for test purpose only. Always set to False in production.
    enable_self_consumption: bool = False,
):
    logging.info("========================================")
    logging.info("Start dispatch loop")
    logging.info("========================================")

    while True:
        error = shared_device_info.get_error()
        if error:
            # if there is an error from oher thread, stop the program
            logging.error(f"====================")
            logging.error(f"critical error: {error}")
            logging.error(f"====================")
            return
        try:
            dispatch_info = shared_device_info.get_first_dispatch()
            if dispatch_info is None:
                # logging.info("No dispatch request")
                await asyncio.sleep(1)
            else:
                logging.error("========================================")
                logging.info("Invoek dispatch request")
                # length_of_queue = shared_device_info.len_dispatch_queue()
                # if we want to get dispatch time from TESS
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
                    if time_to_wait % 10 == 0:
                        logging.info(
                            f"Waiting for dispatch...{time_to_wait}")
                    time_to_wait -= 1
                logging.info(
                    f"Reach dispatch time at {int(time.time())}, dispatch_timestapm : {dispatch_timestamp}.")

                response_message = await submit_dispatch_to_vtn(
                    vtn_dispatch_url=vtn_dispatch_url,
                    order_id=order_id,
                    quantity=quantity,

                )

                if 'quantity' in response_message:
                    logging.info("======= Start to control devices ======")
                    quantity = response_message['quantity']
                    # logging.info(f"Dispatch response: {response_message}")
                    await send_dispatch_quantity_to_devices(
                        device_settings=shared_device_info.get_device_settings(),
                        device_type=shared_device_info.get_device_type(),
                        dispatch_quantity=float(quantity),
                        is_using_mock_device=shared_device_info.get_is_using_mock_device(),
                        emulated_device_api_url=shared_device_info.get_emulated_device_api_url(),

                        enable_self_consumption=enable_self_consumption,

                    )
                else:
                    logging.info("========================================")
                    logging.info(
                        f"Submit dispatch to VTN failed {response_message}, no quantity in response. Do nothing.")
                    logging.info("========================================")
        except Exception as e:
            error_messge = f" handle dispatch error: {e}"
            shared_device_info.set_error(error=error_messge)
            break
