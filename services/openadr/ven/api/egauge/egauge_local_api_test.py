
import datetime
from xml.etree import ElementTree as ET
import requests
from requests.auth import HTTPDigestAuth
import time
import json
import xmltodict
import os
from os.path import join, dirname
# losad data from .evn
from dotenv import load_dotenv, find_dotenv
load_dotenv()

user = os.environ.get("egauge_user")
password = os.environ.get("egauge_password")
url240 = os.environ.get("egauge_url240")
mode = "web"  # or ip
endpoint = os.environ.get("egauge_endpoint")

if user is None:
    raise ValueError("user is None")
if password is None:
    raise ValueError("password is None")
if url240 is None:
    raise ValueError("url240 is None")
if endpoint is None:
    raise ValueError("endpoint is None")


class EgaugeInterface():

    def __init__(self, mode=None, endpoint=None, username=None, password=None, t_sample=5, topic=None, clientid=None):
        # Initializing credentials
        self.endpoint = endpoint
        self.mode = mode
        self.username = username
        self.password = password
        self.TOPIC_PUBLISH_EGAUGE = topic
        self.CLIENT_ID = clientid

        # Initializing parameters
        self.t_sample = t_sample
        self.keys = ["A.Battery", "A.SubPanel",
                     "A.GridPower", "A.Solar", "A.EV", "ts"]

    # Function to process data from e-gauge and convert to useful power values
    def processing_egauge_data(self):
        if self.endpoint == None:
            print('enpoint is None')
            return 'Error egauge: endpoint is none'
        self.url = 'http://' + self.endpoint + '/cgi-bin/egauge?ins&tot'
        power_values = dict.fromkeys(self.keys, None)
        try:
            if self.mode == 'web':
                resp = requests.get(self.url, auth=HTTPDigestAuth(
                    self.username, self.password))
            elif self.mode == 'ip':
                resp = requests.get(self.url)
            else:
                print('mode type not acceptable')
                return 'Error egauge: mode type not acceptable'

            resp.raise_for_status()
            data_ini = self.get_egauge_registers(resp)

        except requests.exceptions.HTTPError as err:
            print(err)
            return json.dumps(power_values)

        time.sleep(self.t_sample)

        try:
            if self.mode == 'web':
                resp = requests.get(self.url, auth=HTTPDigestAuth(
                    self.username, self.password))
                resp.raise_for_status()
            elif self.mode == 'ip':
                resp = requests.get(self.url)
                resp.raise_for_status()
            else:
                print('mode type not acceptable')
                return 'Error egauge: mode type not acceptable'

            data_end = self.get_egauge_registers(resp)

        except requests.exceptions.HTTPError as err:
            print(err)
            return json.dumps(power_values)

        ts_delta = data_end['ts'] - data_ini['ts']
        try:
            for i in power_values:
                if i == 'ts':
                    power_values['ts'] = datetime.datetime.fromtimestamp(
                        int(data_end['ts'])).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    power_values[i] = round(
                        ((data_end[i] - data_ini[i]) / ts_delta) / 1000, 3)

            json_dict = json.dumps(power_values)
            # print('Data Dict: ', json_dict)
            return power_values
        except Exception as e:
            print('Error retrieving data from E-Gauge API: ', e)
            return ('Error egauge: mode type not acceptable', e)

    def get_egauge_registers(self, response):
        power_values = dict.fromkeys(self.keys, None)
        data = xmltodict.parse(response.text)
        data_json = json.loads(json.dumps(data))
        # print('data: ', data_json)
        keys_set = self.keys
        if data_json['data']['ts'] != None:
            power_values['ts'] = int(data_json['data']['ts'])
        egauge_vals = data_json['data']['r']
        # print('egauge_vals: ', egauge_vals)

        for i in egauge_vals:
            if i['@n'] in keys_set:
                power_values[i['@n']] = int(i['v'])

        return power_values


if __name__ == "__main__":

    # retval = EgaugeInterface(mode=mode, endpoint=endpoint,
    #                          username=user, password=password).processing_egauge_data()
    # print(f"retval {retval}")
    while True:
        retval = EgaugeInterface(mode=mode, endpoint=endpoint,
                                 username=user, password=password).processing_egauge_data()
        print(f"retval {retval}, time {datetime.datetime.now()}")
        time.sleep(5)
