from .Sonnen_Battery_Enum import SonnenBatteryAttributeKey, SonnenBatterySystemStatus
from enum import Enum
from datetime import datetime


def convert_sonnen_data_to_openadr_report_format(batt_staus: dict) -> list:
    """
    Get battery status and convert to the openADR historical report format
    Since openADR protocol not allow to pass json format, we have to pass the
    data in an array with [(datetime, value)] format. The value is float type.
    It's important to keep the same sequence, then the VTN can parse correctly.
    Otherwise, VTN may get wrong data.
    Original json format

    {
        "BackupBuffer": "10", "BatteryCharging": true, "BatteryDischarging": false,
        "Consumption_Avg": 0, "Consumption_W": 0, "Fac": 60, "FlowConsumptionBattery": false,
        "FlowConsumptionGrid": false, "FlowConsumptionProduction": false, "FlowGridBattery": true,
        "FlowProductionBattery": true, "FlowProductionGrid": true, "GridFeedIn_W": 196,
        "IsSystemInstalled": 1, "OperatingMode": "2", "Pac_total_W": -1800,
        "Production_W": 1792, "RSOC": 52, "RemainingCapacity_W": 5432, "SystemStatus": "OnGrid",
        "Timestamp": "2023-02-09 14:50:32", "USOC": 49, "Uac": 237, "Ubat": 54
    }

    convert to 
    [(datetime.datetime(2023, 2, 9, 14, 50, 32), '10'), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1), (datetime.datetime(2023, 2, 9, 14, 50, 32), 0), (datetime.datetime(2023, 2, 9, 14, 50, 32), 0), (datetime.datetime(2023, 2, 9, 14, 50, 32), 60), (datetime.datetime(2023, 2, 9, 14, 50, 32), 0), (datetime.datetime(2023, 2, 9, 14, 50, 32), 0), (datetime.datetime(2023, 2, 9, 14, 50, 32), 0), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1), (datetime.datetime(2023, 2, 9, 14, 50, 32), 196), (datetime.datetime(2023, 2, 9, 14, 50, 32), '2'), (datetime.datetime(2023, 2, 9, 14, 50, 32), -1800), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1792), (datetime.datetime(2023, 2, 9, 14, 50, 32), 5432), (datetime.datetime(2023, 2, 9, 14, 50, 32), 1), (datetime.datetime(2023, 2, 9, 14, 50, 32), 49), (datetime.datetime(2023, 2, 9, 14, 50, 32), 237), (datetime.datetime(2023, 2, 9, 14, 50, 32), 54)]

    """
    try:
        index = 0
        report_data = []
        print("batt_staus", batt_staus)
        # check if length of data is larger than length of SonnenBatteryAttributeKey
        if len(batt_staus) < len(SonnenBatteryAttributeKey):
            raise ValueError(
                f"length of data is smaller than length of SonnenBatteryAttributeKey")

        # check if Timestamp is in the data
        if SonnenBatteryAttributeKey.Timestamp.name not in batt_staus:
            raise ValueError(
                f"Timestamp is not in the data")
        timestamp_str = batt_staus[SonnenBatteryAttributeKey.Timestamp.name]
        datetime_object = datetime.strptime(
            timestamp_str, "%Y-%m-%d %H:%M:%S")

        # loop through the SonnenBatteryAttributeKey
        # in the loop, we only preserve the data that is defined in SonnenBatteryAttributeKey
        for key in SonnenBatteryAttributeKey:
            # check if the key is in the data
            if key.name in batt_staus:
                # if yes, get the value
                value = batt_staus[key.name]
                # check if key.name is SonnenBatteryAttributeKey.Timestamp.name then pass:
                if key.name == SonnenBatteryAttributeKey.Timestamp.name:
                    pass
                elif key.name == SonnenBatteryAttributeKey.SystemStatus.name:
                    # the value of SystemStatus is SonnenBatterySystemStatus is OnGrid or OffGrid
                    # convert the value to 1 or 0
                    if value == SonnenBatterySystemStatus.OnGrid.name:
                        new_value = 1
                    elif value == SonnenBatterySystemStatus.OffGrid.name:
                        new_value = 0
                    else:
                        raise ValueError(
                            f"Wops!! SonnenBatterySystemStatus key error {value}")
                    # add value to the report_data
                    report_data.append((datetime_object, new_value))
                elif isinstance(value, bool):
                    # if the value is bool, convert to int
                    if value:
                        new_value = 1
                    else:
                        new_value = 0
                    # add value to the report_data
                    report_data.append((datetime_object, new_value))
                elif isinstance(value, (float, int)):
                    report_data.append((datetime_object, value))
                # elif value is numeric:
                elif value.isnumeric():
                    new_value = float(value)
                    report_data.append((datetime_object, value))
                index += 1
            # if not, raise ValueError
            else:
                raise ValueError(
                    f"key {key.name} is not in the data, please check api definition")
        return report_data

    except Exception as e:
        raise e
