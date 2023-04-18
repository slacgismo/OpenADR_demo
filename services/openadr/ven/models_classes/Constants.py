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


class OrdersAttributes(Enum):
    ORDER_ID = 'order_id'
    PRICE = 'price'
    AUTION_ID = 'auction_id'
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'


class ReadingsTableAttributes(Enum):
    READING_ID = "reading_id"
    METER_ID = "meter_id"
    NAME = "name"
    VALUE = "value"


class MetersTableAttributes(Enum):
    DEVICE_ID = "device_id"
    METER_ID = "meter_id"
    RESOURCE_ID = "resource_id"
    STATUS = "status"


# class ORER_KEYS(Enum):
#     ORDER_ID = 'order_id'
#     PRICE = 'price'
#     AUTION_ID = 'auction_id'
#     QUANTITY = 'quantity'
#     DEVICE_ID = 'device_id'
#     RESOURCE_ID = 'resource_id'
#     RECORD_TIME = 'record_time'
#     FLEXIBLE = 'flexible'
#     STATE = 'state'
