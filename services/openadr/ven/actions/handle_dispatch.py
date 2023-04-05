
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import logging
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributeKey
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface


async def handle_dispatch(
    device_settings: dict = None,
    device_type: str = None,
    dispatch_quantity: int = None,
    is_using_mock_device: bool = False,
    emulated_device_api_url: str = None,
    # this is for test only # always set to False in production, However, i
    enable_self_consumption: bool = False,
):
    """
    Handle a dispatch request.
    enable_self_consumption is for test only. Always set to False in production.
    However, when you done with battery test, you have to set it to True to prevent the battery from fully discharging.
    """
    if dispatch_quantity is None:
        raise Exception("dispatch_quantity is None")

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
                    #
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
                    logging.info(f"enable_manual_mode response: {response}")
                    if response['status'] == "0":
                        if dispatch_quantity > 0:
                            mode = 'discharge'
                        else:
                            mode = 'charge'
                        logging.info(
                            "enable_manual_mode success")
                        manul_mode_control_response = await battery_interface.manual_mode_control(
                            mode=mode, value=str(dispatch_quantity))
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
