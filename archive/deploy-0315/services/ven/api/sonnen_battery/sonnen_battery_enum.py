from enum import Enum


class SonnenBatteryOperatingMode(Enum):
    TimeofUseMode = 10
    ManualMode = 1
    SelfConsumptionMode = 2
    BackupMode = 7


class SonnenBatterySystemStatus(Enum):
    OnGrid = 1
    OffGrid = 0


class SonnenBatteryAttributeKey(Enum):
    BackupBuffer = 0
    BatteryCharging = 1
    BatteryDischarging = 2
    # Consumption_Avg # exist but unused data
    Consumption_W = 3
    Fac = 4
    FlowConsumptionBattery = 5
    FlowConsumptionGrid = 6
    FlowConsumptionProduction = 7
    FlowGridBattery = 8
    FlowProductionBattery = 9
    FlowProductionGrid = 10
    GridFeedIn_W = 11
    # IsSystemInstalled  # exist but unused data
    OperatingMode = 12
    Pac_total_W = 13
    Production_W = 14
    # RSOC # exist but unused data
    RemainingCapacity_W = 15
    SystemStatus = 16
    USOC = 17
    Uac = 18
    Ubat = 19
    Timestamp = 'Timestamp'
