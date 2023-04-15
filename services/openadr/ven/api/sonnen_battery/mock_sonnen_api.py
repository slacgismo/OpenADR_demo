
import requests
import json
# import numpy as np

# import pandas as pd
from .sonnen_data_converter import convert_sonnen_data_to_openadr_report_format
# from dataclasses import dataclass


class MockSonnenInterface():

    def __init__(self, serial: str = None, auth_token: str = None, url_ini=None, device_brand: str = None):
        self.serial = serial
        self.token = auth_token
        self.url_ini = url_ini
        self.device_brand = device_brand
        self.headers = {'Accept': 'application/vnd.sonnenbatterie.api.core.v1+json',
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + self.token, }

    async def get_mock_battery_status(self):

        try:

            # Encode the payload data as UTF-8 encoded JSON

            resp = requests.get(
                self.url_ini + f"/{self.serial}?device_brand={ self.device_brand}")

            batt_staus = resp.json()
            print("======   get_mock_battery_status   ======")
            print(batt_staus)
            print("------------------------------------------")
            return batt_staus

        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

    # async def get_status_and_convert_to_openleadr_report(self):
    #     """
    #     Get battery status and convert to the openADR historical report format
    #     Since openADR protocol not allow to pass json format, we have to pass the
    #     data in an array with [(datetime, value)] format. The value is float type.
    #     It's important to keep the same sequence, then the VTN can parse correctly.
    #     Otherwise, VTN may get wrong data.
    #     Original json format

    #     {
    #         "BackupBuffer": "10", "BatteryCharging": true, "BatteryDischarging": false,
    #         "Consumption_Avg": 0, "Consumption_W": 0, "Fac": 60, "FlowConsumptionBattery": false,
    #         "FlowConsumptionGrid": false, "FlowConsumptionProduction": false, "FlowGridBattery": true,
    #         "FlowProductionBattery": true, "FlowProductionGrid": true, "GridFeedIn_W": 196,
    #         "IsSystemInstalled": 1, "OperatingMode": "2", "Pac_total_W": -1800,
    #         "Production_W": 1792, "RSOC": 52, "RemainingCapacity_W": 5432, "SystemStatus": "OnGrid",
    #         "Timestamp": "2023-02-09 14:50:32", "USOC": 49, "Uac": 237, "Ubat": 54
    #     }

    #     """
    #     params = {"serial": self.serial}

    #     try:
    #         resp = requests.get(self.url_ini, params=params,
    #                             headers=self.headers)
    #         resp.raise_for_status()
    #     except requests.exceptions.HTTPError as err:
    #         print(err)
    #         return requests.exceptions.HTTPError

    #     try:
    #         batt_staus = resp.json()

    #         # convert to openADR report format
    #         battery_data = convert_sonnen_data_to_openadr_report_format(
    #             batt_staus)
    #         return battery_data
    #     except ValueError as e:
    #         raise (f"convert to openADR report error:{e} ")

    # Backup:
    # Intended to maintain an energy reserve for situations where the Grid is no longer available. During the off-grid
    # period the energy would be dispensed to supply the demand of power from all the essential loads.
    # Load management can be enabled to further extend the life of the batteries by the Developers.

    async def enable_backup_mode(self):

        return "enable backup mode"

    # Self-Consumption:
    # The ecoLinx monitors all energy sources (Grid, PV, Generator), loads, and Energy Reserve Percentage
    # in order to minimize purchase of energy from the Grid.

    async def enable_self_consumption(self):
        # now it seems 8 converts internally to 2 (test and update the code)

        return "enable self consumption"

    async def powermeter(self):

        return "powermeter"

    async def set_min_soc(self, value=5):

        return "set_min_soc"
    # Time of Use (TOU):
    # This mode allows users to set time windows where it is preferred to employ the use of stored energy
    # (from PV) rather than consume from the grid.

    async def enable_tou(self):
        return "enable_tou"

    async def tou_grid_feedin(self, value=0):
        # value = 0 disable charging from grid
        # value = 1 enable charging from grid

        return "tou_grid_feedin"

    async def tou_window(self, pk_start='[16:00]', pk_end='[21:00]', opk_start='[21:01]'):
        # value format = [HH:00] in 24hrs format

        return "tou_window"

    # Manual Mode
    # This mode allows the user to manually charge or discharge the batteries. The user needs to provide the
    # value for charging or discharging and based on the value, the ecoLinx system will charge until it reaches
    # 100% or discharge until it reaches 0% User SOC (unless stopped by the user by changing the charge/discharge
    # value to 0).

    # Enabled by default
    async def enable_manual_mode(self):
        try:

            resp = requests.get(
                self.url_ini + f"/{self.serial}?device_brand={self.device_brand}&enable_manual_mode=1", headers=self.headers)

            body = resp.json()
            if 'status' in body:
                return body['status']
            else:
                return {'status': '1'}

        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

    async def manual_mode_control(self, mode='charge', value='0'):
        try:
            resp = requests.get(
                self.url_ini + f"/{self.serial}?device_brand={self.device_brand}&manual_mode_control=1", headers=self.headers)

            body = resp.json()
            if 'ReturnCode' in body:
                return body['ReturnCode']
            else:
                return {'ReturnCode': '1'}

        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

    async def enable_self_consumption(self):
        return {"status": "0"}
