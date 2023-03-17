from enum import Enum


class DEVICE_TYPES(Enum):
    HS = 'HS'   # Battery Storage
    PV = 'PV'
    EV = 'EV'   # Electric Vehicle
    HC = 'HC'


class BATTERY_BRANDS(Enum):
    SONNEN_BATTERY = 'SONNEN_BATTERY'
    E_GUAGE = 'E_GUAGE'
