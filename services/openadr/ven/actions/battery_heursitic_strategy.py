
"""
Calculate the power price for the battery heuristic strategy.
"""
from statistics import NormalDist
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
