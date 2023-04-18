from enum import Enum


class SonnenBatteryOperatingMode(Enum):
    TimeofUseMode = 10
    ManualMode = 1
    SelfConsumptionMode = 2
    BackupMode = 7


class SonnenBatterySystemStatus(Enum):
    OnGrid = 1
    OffGrid = 0


class SonnenBatteryAttributes(Enum):
    BackupBuffer = 'BackupBuffer'
    BatteryCharging = 'BatteryCharging'
    BatteryDischarging = 'BatteryDischarging'
    # Consumption_Avg # exist but unused data
    Consumption_W = 'Consumption_W'
    Fac = 'Fac'
    FlowConsumptionBattery = 'FlowConsumptionBattery'
    FlowConsumptionGrid = 'FlowConsumptionGrid'
    FlowConsumptionProduction = 'FlowConsumptionProduction'
    FlowGridBattery = 'FlowGridBattery'
    FlowProductionBattery = 'FlowProductionBattery'
    FlowProductionGrid = 'FlowProductionGrid'
    GridFeedIn_W = 'GridFeedIn_W'
    # IsSystemInstalled  # exist but unused data
    OperatingMode = 'OperatingMode'
    Pac_total_W = 'Pac_total_W'
    Production_W = 'Production_W'
    # RSOC # exist but unused data
    RemainingCapacity_W = 'RemainingCapacity_W'
    SystemStatus = 'SystemStatus'
    USOC = 'USOC'
    Uac = 'Uac'
    Ubat = 'Ubat'
    Timestamp = 'Timestamp'
