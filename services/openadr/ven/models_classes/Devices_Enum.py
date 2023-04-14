from enum import Enum


class DEVICE_TYPES(Enum):
    ES = 'ES'   # Battery Storage
    PV = 'PV'
    EV = 'EV'   # Electric Vehicle
    HC = 'HC'


class BATTERY_BRANDS(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'


class SONNEN_BATTERY_DEVICE_SETTINGS(Enum):
    BATTERY_SN = 'battery_sn'
    BATTERY_TOKEN = 'battery_token'
    DEVICE_BRAND = 'device_brand'
    FLEXIBLE = 'flexible'
    IS_USING_MOCK_DEVICE = 'is_using_mock_device'
