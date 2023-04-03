
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import logging
from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributeKey
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface


async def handle_dispatch(
    device_settings: dict = None,
    device_type: str = None,
    is_using_mock_device: bool = False,
    emulated_device_api_url: str = None
):
    """
    Handle a dispatch request.
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
                    # get battery data from mock device
                    # batter_data = await mock_battery_interface.get_mock_battery_status()

                else:
                    logging.info(
                        "======== Send dispatch to real battery ==================")
                    battery_interface = SonnenInterface(
                        serial=battery_sn, auth_token=battery_token)
                    # get battery data from device
                    # batter_data = await battery_interface.get_status()
            else:
                raise Exception(
                    f"Device brand {device_brand} is not supported yet")
        except Exception as e:
            raise Exception(f"Error getting battery data from API: {e}")
    else:
        raise Exception(f"Device type {device_type} is not supported yet")
