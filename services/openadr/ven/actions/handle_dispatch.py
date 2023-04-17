
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import logging
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
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
import logging
import time
import logging
import time
import aiohttp


async def handle_dispatch(
    vtn_dispatch_url: str = None,
    shared_device_info: SharedDeviceInfo = None,
    # enable_self_consumption is to prevent battery fully discharge. Setup to Truen when finish test, this is for test purpose only. Always set to False in production.
    enable_self_consumption: bool = False,
):
    logging.info("========================================")
    logging.info("Start dispatch loop")
    logging.info("========================================")
    ven_id = shared_device_info.get_ven_id()
    while True:
        error = shared_device_info.get_error()
        if error:
            # if there is an error from oher thread, stop the program
            logging.error(f"critical error: {error}")
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
                    logging.info(f"Dispatch response: {response_message}")
                    await send_dispatch_quantity_to_device(
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
                    await control_sonnen_battery(
                        battery_interface=mock_battery_interface,
                        quantity=dispatch_quantity,
                        enable_self_consumption=enable_self_consumption,

                    )

                else:

                    logging.info(
                        "======== Send dispatch to real battery ==================")
                    battery_interface = SonnenInterface(
                        serial=battery_sn, auth_token=battery_token)

                    await control_sonnen_battery(
                        battery_interface=battery_interface,
                        quantity=dispatch_quantity,
                        enable_self_consumption=enable_self_consumption,

                    )

            else:
                raise Exception(
                    f"Device brand {device_brand} is not supported yet")
        except Exception as e:
            raise Exception(f"Error getting battery data from API: {e}")
    else:
        raise Exception(f"Device type {device_type} is not supported yet")


async def control_sonnen_battery(battery_interface, quantity: float, enable_self_consumption: bool = False):
    """
    battery_interface is the interface to the battery. It can be a real battery or a mock battery.
    Mock battery interface is for test only.

    """
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
        if quantity < 0:
            mode = 'discharge'
        else:
            mode = 'charge'

        logging.info(
            "enable_manual_mode success")
        manul_mode_control_response = await battery_interface.manual_mode_control(
            mode=mode, value=str(abs(quantity)))  # remmeber to use absouute value since we already check the mode
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


async def submit_dispatch_to_vtn(
    vtn_dispatch_url: str = None,
    order_id: str = None,
    quantity: float = None,
):
    url = vtn_dispatch_url
    dispatch_data = {
        "order_id": order_id,
        "record_time": int(time.time()),
        "quantity": str(quantity)
    }

    headers = {'Content-Type': 'application/json'}
    logging.info("submit_dispatch_to_lambda ")
    async with aiohttp.ClientSession() as session:
        async with session.put(vtn_dispatch_url, json=dispatch_data, timeout=2, headers=headers) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                text = await response.text()
                logging.error(
                    f"Unexpected content type: {content_type} {text}")
                raise Exception(f"Unexpected content type: {content_type}")
            if response.status != 200:
                logging.info(f"Error submit order to TESS:{response} ")
                raise Exception(
                    f"Error submit order to TESS: {response.status}")
            return await response.json()
