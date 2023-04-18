import logging


from .Sonnen_Battery_Enum import SonnenBatteryAttributes


async def filter_battery_data(battery_data: dict) -> dict:

    filtered_battery_data = battery_data
    if len(battery_data) < len(SonnenBatteryAttributes):
        raise ValueError(
            f"length of data is smaller than length of SonnenBatteryAttributes")
    remove_keys = []
    # find the keys that are not in SonnenBatteryAttributes
    for key, value in battery_data.items():
        if key not in [key.name for key in SonnenBatteryAttributes]:
            remove_keys.append(key)

    # Remove the keys value from the data that are not in SonnenBatteryAttributes
    for key in remove_keys:
        filtered_battery_data.pop(key)
        # logging.info('pop key: ' + key)
    return filtered_battery_data
