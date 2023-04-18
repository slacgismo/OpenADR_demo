
"""
Calculate the power price for the battery heuristic strategy.
"""
from statistics import NormalDist
from enum import Enum
import logging
from models_classes.SharedDeviceInfo import SharedDeviceInfo
from models_classes.Constants import DEVICE_TYPES, BATTERY_BRANDS, SONNEN_BATTERY_DEVICE_SETTINGS
from api.sonnen_battery.Sonnen_Battery_Enum import SonnenBatteryAttributes

from helper.guid import guid


class ORER_KEYS(Enum):
    ORDER_ID = 'order_id'
    PRICE = 'price'
    AUTION_ID = 'auction_id'
    QUANTITY = 'quantity'
    DEVICE_ID = 'device_id'
    RESOURCE_ID = 'resource_id'
    RECORD_TIME = 'record_time'
    FLEXIBLE = 'flexible'
    STATE = 'state'


# Battery heursitic strategy
# variable = value [units] [source]
Pmean = 50      # $/MWh auction
Pstdev = 5       # $/MWh auction
Pmin = 0        # $/MWh resources   # min price of the market
Pmax = 100      # $/MWh resources # max price of the market
tclear = 0.083  # h     resources
Kes = 1     # none  participant
Qdesired = 80  # kWh   participant
Qmin = 20       # kWh   participant
Qmax = 95       # kWh   participant
Qcap = 100      # kWh   participant
dQmax = 6       # kW    participant
# Calculate the battery heursitic strategy
# calculate power order quantity

# sudo code
# we need USOC here , from customer desired USOC random from 40 to 80 percent
# if USOC < desired_USOC and USOC > Qmin:
# quantity is the max charging capacity of battery
# quantity is charging, it's positive.
# Price
# Porder = gussiasn_function(inverer_normal, Pmean = Aution_Table(expected_price), 3*Kes(from customers UI/UX), Pstedev = Aution_Table(expected_stdev), (1- (Qlast = USOC - Qmin = (customer from UI/UX)))/2*(Qdesired = desired_USOC,  Qmin = (customer from UI/UX)))))``
# elif USOC > desired_USOC or USOC < Qmax:
# quantity is the max discharging capacity of battery
# quantity is discharging, it's negative.
# Porder = gussiasn_function(inverer_normal, Pmean = Aution_Table(expected_price), 3*Kes(from customers UI/UX), Pstedev = Aution_Table(expected_stdev), (1- (Qmax = (from customer UI/UX) - Qlast = USOC )/Qmax = (from customer UI/UX) - Qdesided =  desired_USOC))
# qual: do nothing.

# 1. desied_USOC from customers UI/UX paticipant
# 2. Qmin
# 3. Qmax
# 4. Pmean = Aution_Table(expected_price)
# 5. Pstedev = Aution_Table(expected_stdev)
# 6. Kes(from customers UI/UX)  paticipant
# 7. Qlast = USOC from  paticipant


def power_quantity(Qdesired, Qmin, Qmax, Qcap, Qlast, dQmax):
    Qorder = 0
    if Qlast < Qdesired:
        Qorder = dQmax
    elif Qlast > Qdesired:
        Qorder = -dQmax
    return Qorder
# calculate power order price


def power_price(Pmean, Pstdev, Pmin, Pmax, Qlast, Qdesired, Qmin, Qmax, Kes):
    Porder = 0
    if Qdesired < Qlast < Qmax:
        Porder = NormalDist(
            mu=Pmean, sigma=Kes*Pstdev).inv_cdf((Qmax - Qlast)/(2*(Qmax - Qdesired)))
    elif Qlast <= Qmin:
        Porder = Pmax
    elif Qlast >= Qmax:
        Porder = Pmin
    elif Qmin < Qlast <= Qdesired:
        Porder = NormalDist(
            mu=Pmean, sigma=Kes*Pstdev).inv_cdf(1 - (Qlast - Qmin)/(2*(Qdesired - Qmin)))
    if Porder > Pmax:
        Porder = Pmax
    elif Porder < Pmin:
        Porder = Pmin
    return Porder


def convert_device_data_to_order_data(
        device_data: dict = None,
        device_type: str = None,
        deivce_brand: str = None,
        simulation_oder_json_file='./actions/dump_orders.json',
        market_interval: int = 60,
):
    if device_data is None:
        raise Exception("device_data cannot be None")

    if device_type is None:
        raise Exception("device_type cannot be None")

    shared_device_info = SharedDeviceInfo.get_instance()
    device_id = shared_device_info.get_device_id()
    resource_id = shared_device_info.get_resource_id()
    flexible = shared_device_info.get_flexible()
    # find the recod time
    record_time = None
    state = None
    quantity = None
    price = None
    aution_id = None
    order_id = None

    if device_type == DEVICE_TYPES.ES.value:
        if deivce_brand == BATTERY_BRANDS.SONNEN_BATTERY.value:
            if SonnenBatteryAttributes.Timestamp.name in device_data:
                # TODO: fetch necesary data from TESS API
                Pmean = 50      # $/MWh auction return from lambd APi and get from simulator
                Pstdev = 5       # $/MWh auction return from lambd APi and get from  simulator
                Pmin = 0        # $/MWh resources
                Pmax = 100      # $/MWh resources
                Kes = 1     # none  participant
                Qdesired = 80  # kWh   participant
                Qmin = 20       # kWh   participant # min charging or discharging capacity of battery
                Qmax = 95       # kWh   participant # max charging or discharging capacity of battery
                Qcap = 100      # kWh   participant
                dQmax = 6       # kW    participant
                # Qlast = last state of USOC
                Qlast = device_data[SonnenBatteryAttributes.USOC.name]
                # verify the code
                # Qsoc_last = 55 quantity = 6 price = 52.742611413490486
                #
                # first get the power quantity
                # quantity = "1000"
                quantity = power_quantity(
                    Qdesired=Qdesired,
                    Qmin=Qmin,
                    Qmax=Qmax,
                    Qcap=Qcap,
                    Qlast=Qlast,
                    dQmax=dQmax,
                )
                # Second get the price
                price = power_price(
                    Pmean=Pmean,
                    Pstdev=Pstdev,
                    Pmin=Pmin,
                    Pmax=Pmax,
                    Qlast=Qlast,
                    Qdesired=Qdesired,
                    Qmin=Qmin,
                    Qmax=Qmax,
                    Kes=Kes,

                )

                logging.warning(
                    f"-----------  quantity  {quantity} W, price is {price} -----------")
                state = device_data[SonnenBatteryAttributes.Pac_total_W.name]
                # price = "1.2"

                order_id = str(guid())
            else:
                raise Exception("timestamp is not in device_data")
        else:
            raise Exception(
                "device_brand is not supported, please implement it")

    order_data = {
        ORER_KEYS.ORDER_ID.value: order_id,
        ORER_KEYS.DEVICE_ID.value: device_id,
        ORER_KEYS.RESOURCE_ID.value: resource_id,
        ORER_KEYS.RECORD_TIME.value: record_time,
        ORER_KEYS.FLEXIBLE.value: flexible,
        ORER_KEYS.STATE.value: state,
        ORER_KEYS.QUANTITY.value: quantity,
        ORER_KEYS.PRICE.value: price,
        ORER_KEYS.AUTION_ID.value: aution_id
    }

    return order_data
