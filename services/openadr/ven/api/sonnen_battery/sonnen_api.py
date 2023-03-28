import datetime
from xml.etree import ElementTree as ET
import requests
from requests.auth import HTTPDigestAuth
# import numpy as np
import time
import json
# import pandas as pd
import time as t
import os
from datetime import datetime
from .sonnen_data_converter import convert_sonnen_data_to_openadr_report_format
import types
# from dataclasses import dataclass


class SonnenInterface():

    def __init__(self, serial=None, auth_token=None):
        self.serial = serial
        self.token = auth_token
        self.url_ini = 'https://core-api.sonnenbatterie.de/proxy/'
        self.headers = {'Accept': 'application/vnd.sonnenbatterie.api.core.v1+json',
                        'Authorization': 'Bearer ' + self.token, }

    def get_status(self):
        status_endpoint = '/api/v1/status'

        try:
            resp = requests.get(self.url_ini + self.serial +
                                status_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def get_status_and_convert_to_openleadr_report(self):
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

        """
        status_endpoint = '/api/v1/status'

        try:
            resp = requests.get(self.url_ini + self.serial +
                                status_endpoint, headers=self.headers)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            return requests.exceptions.HTTPError

        try:
            batt_staus = resp.json()

            # convert to openADR report format
            report_data = convert_sonnen_data_to_openadr_report_format(
                batt_staus)
            # print("-------- battery_data", report_data)
            return report_data
        except ValueError as e:
            raise (f"convert to openADR report error:{e} ")

    # Backup:
    # Intended to maintain an energy reserve for situations where the Grid is no longer available. During the off-grid
    # period the energy would be dispensed to supply the demand of power from all the essential loads.
    # Load management can be enabled to further extend the life of the batteries by the Developers.

    def enable_backup_mode(self):
        backup_endpoint = '/api/setting?EM_OperatingMode=7'
        try:
            resp = requests.get(self.url_ini + self.serial +
                                backup_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    # Self-Consumption:
    # The ecoLinx monitors all energy sources (Grid, PV, Generator), loads, and Energy Reserve Percentage
    # in order to minimize purchase of energy from the Grid.

    def enable_self_consumption(self):
        # now it seems 8 converts internally to 2 (test and update the code)
        sc_endpoint = '/api/setting?EM_OperatingMode=2'
        try:
            resp = requests.get(self.url_ini + self.serial +
                                sc_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def powermeter(self):
        sc_endpoint = '/api/powermeter'
        try:
            resp = requests.get(self.url_ini + self.serial +
                                sc_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def set_min_soc(self, value=5):
        sc_endpoint = '/api/setting?EM_USOC='+str(value)
        try:
            resp = requests.get(self.url_ini + self.serial +
                                sc_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()
    # Time of Use (TOU):
    # This mode allows users to set time windows where it is preferred to employ the use of stored energy
    # (from PV) rather than consume from the grid.

    def enable_tou(self):
        tou_endpoint = '/api/setting?EM_OperatingMode=10'
        try:
            resp = requests.get(self.url_ini + self.serial +
                                tou_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def tou_grid_feedin(self, value=0):
        # value = 0 disable charging from grid
        # value = 1 enable charging from grid
        grid_feedin_endpoint = '/api/setting?EM_US_GRID_ENABLED=' + str(value)
        try:
            resp = requests.get(self.url_ini + self.serial +
                                grid_feedin_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def tou_window(self, pk_start='[16:00]', pk_end='[21:00]', opk_start='[21:01]'):
        # value format = [HH:00] in 24hrs format
        tou_pk_start_endpoint = '/api/setting?EM_US_PEAK_HOUR_START_TIME=' + pk_start
        tou_pk_end_endpoint = '/api/setting?EM_US_PEAK_HOUR_END_TIME=' + pk_end
        tou_opk_start_endpoint = '/api/setting?EM_US_LOW_TARIFF_CHARGE_TIME=' + opk_start
        try:
            resp1 = requests.get(self.url_ini + self.serial +
                                 tou_pk_start_endpoint, headers=self.headers)
            resp1.raise_for_status()
            resp2 = requests.get(self.url_ini + self.serial +
                                 tou_pk_end_endpoint, headers=self.headers)
            resp2.raise_for_status()
            resp3 = requests.get(self.url_ini + self.serial +
                                 tou_opk_start_endpoint, headers=self.headers)
            resp3.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return [resp1.json(), resp2.json(), resp3.json()]

    # Manual Mode
    # This mode allows the user to manually charge or discharge the batteries. The user needs to provide the
    # value for charging or discharging and based on the value, the ecoLinx system will charge until it reaches
    # 100% or discharge until it reaches 0% User SOC (unless stopped by the user by changing the charge/discharge
    # value to 0).

    # Enabled by default
    def enable_manual_mode(self):
        manual_endpoint = '/api/setting?EM_OperatingMode=1'
        try:
            resp = requests.get(self.url_ini + self.serial +
                                manual_endpoint, headers=self.headers)
            resp.raise_for_status()

        except requests.exceptions.HTTPError as err:
            print(err)

        return resp.json()

    def manual_mode_control(self, mode='charge', value='0'):
        control_endpoint = '/api/v1/setpoint/'
        # Checking if system is in off-grid mode
        voltage = SonnenInterface(
            serial=self.serial, auth_token=self.token).get_status()['Uac']

        if voltage == 0:
            print('Battery is in off-grid mode... Cannot execute the command')
            return {}

        else:
            try:
                resp = requests.get(self.url_ini + self.serial + control_endpoint + mode + '/' + value,
                                    headers=self.headers)
                resp.raise_for_status()

            except requests.exceptions.HTTPError as err:
                print(err)

            return resp.json()
