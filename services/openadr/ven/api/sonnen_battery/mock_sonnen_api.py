
import requests
import json
# import numpy as np

# import pandas as pd
# from dataclasses import dataclass
from models_classes.Constants import BATTERY_BRANDS


class MockSonnenInterface():

    def __init__(self, serial: str = None, auth_token: str = None, url_ini=None, device_brand: str = None):
        self.serial = serial
        self.token = auth_token
        self.url_ini = url_ini
        self.device_brand = device_brand
        if self.device_brand != BATTERY_BRANDS.SONNEN_BATTERY.value:
            raise Exception(
                f"device_brand {self.device_brand} is not compatible with MockSonnenInterface class")

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
        '''
        response {
            "enable_manual_mode": 1,
            "status": 0
        }
        '''
        try:

            resp = requests.get(
                self.url_ini + f"/{self.serial}?device_brand={self.device_brand}&enable_manual_mode=1", headers=self.headers)

            return resp.json()
            # if 'status' in body:
            #     return body['status']
            # else:
            #     return {'status': '1'}

        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

    async def manual_mode_control(self, mode='charge', value='0'):
        '''
        response {
            "manual_mode_control": 1,
            "ReturnCode": 0
        }
        '''
        try:
            resp = requests.get(
                self.url_ini + f"/{self.serial}?device_brand={self.device_brand}&manual_mode_control=1", headers=self.headers)

            return resp.json()
            # body = resp.json()
            # if 'ReturnCode' in body:
            #     return body['ReturnCode']
            # else:
            #     return {'ReturnCode': '1'}

        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

    async def enable_self_consumption(self):
        return {"status": "0"}
