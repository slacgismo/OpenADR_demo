from models_classes.Devices_Enum import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.sonnen_api import SonnenInterface
from api.sonnen_battery.mock_sonnen_api import MockSonnenInterface
import logging


async def send_dispatch_quantity_to_devices(
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
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.FLEXIBLE.value:
                    pass
                elif key == SONNEN_BATTERY_DEVICE_SETTINGS.IS_USING_MOCK_DEVICE.value:
                    pass
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
                        serial=battery_sn, auth_token=battery_token, url_ini=emulated_device_api_url, device_brand=device_brand)
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
    if 'status' not in response:
        raise Exception(
            f"enable_manual_mode failed status not in reponse: {response}")
    status = str(response['status'])
    if status == "0":
        if quantity < 0:

            mode = 'discharge'
        else:
            mode = 'charge'

        logging.info(
            "********* enable_manual_mode success *********")

        manul_mode_control_response = await battery_interface.manual_mode_control(
            mode=mode, value=str(abs(quantity)))  # remmeber to use absouute value since we already check the mode
        logging.info(
            f"manul_mode_control_response : {manul_mode_control_response}")
        if 'ReturnCode' in manul_mode_control_response:
            if str(manul_mode_control_response['ReturnCode']) == "0":
                logging.info(
                    f"*********** mode: {mode} quantity: {quantity} manual_mode_control success **************")
            else:
                raise Exception(
                    f"manual_mode_control failed: {manul_mode_control_response}")
        logging.warning(
            "TODO:After the test. Please always enable_self_consumption() to prvent battery from fully discharging"
        )

    else:

        raise Exception(
            f"enable_manual_mode failed: {response}")
