
import uuid
from enum import Enum
import pandas as pd
import random
import csv
from enum import Enum
import os
from typing import List, Dict, Tuple
import pandas as pd
from models_and_classes.SQSService import SQSService
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
import time
import json
"""
This controller app is used to control the worker app for developement and testing purpose.
It will generate following sqs:
1. generate number agents for test purpose
2. destroy number agents

"""
import boto3
from botocore.exceptions import ClientError


class Device_Type(Enum):
    ES = "ES"  # battery
    HC = "HC"
    HW = "HW"
    PV = "PV"  # photovoltaic
    EV = "EV"  # electric vehicle


class Market_Interval(Enum):
    One_Minute = 60
    Five_Miuntes = 300


class BATTERY_BRANDS(Enum):
    SONNEN_BATTERY = "SONNEN_BATTERY"
    E_GUAGE = "E_GUAGE"


class DEVICE_SETTING_KEY(Enum):
    BATTERY_BRANDS = "battery_brand"
    BATTERY_TOKEN = "battery_token"
    BATTEY_SN = "battery_sn"


class DEVICES_KEY(Enum):
    DEVICE_ID = "device_id"
    DEVICE_NAME = "device_name"
    DEVICE_TYPE = "device_type"
    DEVICE_SETTINGS = "device_settings"
    FLEXIBLE = "flexible"
    METER_ID = "meter_id"


class AGNET_KEY(Enum):
    AGENT_ID = "agent_id"
    RESOURCE_ID = "resource_id"
    MARKET_INTERVAL_IN_SECOND = "market_interval_in_second"
    MARKET_ID = "market_id"
    DEVICES = "devices"


def generate_first_number_agents_from_simulation_csv_file(
    market_interval: Market_Interval = Market_Interval.Five_Miuntes,
    number_of_market: int = 2,
    number_of_resouce_per_market: int = 2,
    number_of_agent_per_resource: int = 1,
    device_type: str = Device_Type.ES.value,
    fifo_sqs: str = None,
    ecs_action: str = None,
    ENV: str = None,
    SQS_GROUPID: str = None,

) -> List[Dict]:
    """
    {
    "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
    "resource_id": "caff6719c24359a155a4d0d2f265a7",
    "market_interval_in_second": "300",
    "market_id": "6436a67e184d3694a15886215ae464",
    "devices": [
        {
            "device_id": "807f8e4a37446e80c5756a74a3598d",
            "device_name": "battery_0",
            "device_type": "ES",
            "flexible": "1",
            "meter_id": "6436a67e184d3694a15886215ae464"
            "device_settings": {
                "battery_token": "12321321qsd",
                "battery_sn": "66354",
                "device_brand": "SONNEN_BATTERY"
            },

        }
    ]
    }
    """

    # read csv file
    meters_table_df = convert_csv_to_pandas(
        file="dump_meters.csv", path="./simulation_data_files")

    devices_table_df = convert_csv_to_pandas(
        file="dump_devices.csv", path="./simulation_data_files")
    settings_table_df = convert_csv_to_pandas(
        file="dump_settings.csv", path="./simulation_data_files")
    agents_table_df = convert_csv_to_pandas(
        file="dump_agents.csv", path="./simulation_data_files")
    markets_table_df = convert_csv_to_pandas(
        file="dump_markets.csv", path="./simulation_data_files")
    # create the list of the command to be sent to sqs
    battery_token_df = convert_csv_to_pandas(
        file="simluated_battery.csv", path="./simulation_data_files")
    command_list = []
    # get the market id list hwere the market interval is 60
    market_resources_dict_list, resources_ids = get_market_and_resource_ids(
        dataframe=markets_table_df,
        number_of_market=number_of_market,
        number_of_resouce_per_market=number_of_resouce_per_market, interval=market_interval)
    # print(market_resources_dict_list, resources_ids)

    # find agents id list and the relation between the resource id and the agent id
    resouce_agent_dict_list, agent_id_list = get_resource_agent_relation(
        agents_table_df=agents_table_df,
        resources_ids=resources_ids,
        number_of_agent_per_resource=number_of_agent_per_resource
    )
    # print(resouce_agent_dict_list, agent_id_list)
    # use agnet id list to find the device id list

    agent_device_dict_list, device_id_list = get_agent_device_relation(
        devices_table_df=devices_table_df,
        agent_id_list=agent_id_list,
        device_type=device_type
    )

    meter_device_dict_list, meter_id_list = get_meter_device_relation(
        meters_table_df=meters_table_df,
        device_id_list=device_id_list,
    )

    # print(agent_device_dict_list, device_id_list)

    # combine all relation to create the command list
    command_list = make_command_list(
        market_resources_dict_list=market_resources_dict_list,
        resouce_agent_dict_list=resouce_agent_dict_list,
        agent_device_dict_list=agent_device_dict_list,
        battery_token_df=battery_token_df,
        market_interval_in_second=str(market_interval)
    )
    print(f"length of command {len(command_list)} \n")

    # TODO: check the number of workers, estimate time and the number of workers
    # TODO: if no workers, start the workers, it not enough workers, start more workers
    sqs_messages = create_messages_list(
        command_list=command_list,
        MessageGroupId=SQS_GROUPID,
        ecs_action=ecs_action,
    )
    sqs_service = SQSService(
        queue_url=fifo_sqs,

    )
    # purge the queue
    # sqs_service.purge_message()
    # print("Purge sqs queue")
    # time.sleep(5)
    # create message list

    # TODO: send out the command to sqs queue
    for message in sqs_messages:
        sqs_service.send_message(
            message_body=message['MessageBody'],
            message_attributes=message['MessageAttributes'],
            message_group_id=message['MessageGroupId']
        )
        time.sleep(1)

    print(f"Send out {len(sqs_messages)} sqs messages")
    # TODO: check the status of the workers from the dynamodb table, and wait for the workers to finish


def create_messages_list(
    command_list: List[Dict],
    MessageGroupId: str,
    ecs_action: str = None,
) -> List[Dict]:

    message_attributes = {
        'Action': {'StringValue':  ecs_action, 'DataType': "String"},
        'Services': {'StringValue': 'AWS', 'DataType': "String"},
    }
    deduplication_id = str(guid())
    group_id = MessageGroupId

    # Create a list of SQS messages with attributes, deduplication ID, and group ID
    sqs_messages = [{
        'Id': str(i),
        'MessageBody': json.dumps(message),
        'MessageAttributes': message_attributes,
        'MessageDeduplicationId': deduplication_id,
        'MessageGroupId': MessageGroupId
    } for i, message in enumerate(command_list)]

    return sqs_messages


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


def parse_batteries_csv_file_to_json(
    path: str,
    battery_file: str,
    num_rows: int,
    batter_brands: str
):
    """Parse the battery csv file and return a list of battery token
    "Item1": {
        "serial": {
            "S": "66354"
        },
        "token": {
            "S": "12321321qsd"
        }
    },
    """
    battery_df = convert_csv_to_pandas(file=battery_file, path=path)
    battery_token_list = battery_df["battery_token"][:num_rows].tolist()
    battery_sn_list = battery_df["battery_sn"][:num_rows].tolist()
    battery_brand_list = battery_df["device_brand"][:num_rows].tolist()
    batteries_json = {}
    if len(battery_token_list) < num_rows:
        raise Exception("battery_token_list is not enough")
    # loop through the battery token list and create a json file
    # for index, sen in battery_sn_list:
    for index, sn in enumerate(battery_sn_list):
        if sn == "null":
            raise Exception("battery_sn is null")
        batteries_json[f'Item{index}'] = {

            "token": {"S": battery_token_list[index]},
            "serial": {"S": str(battery_sn_list[index])}
        }
    # save battery to json file
    with (open(f"{path}/batteries.json", "w")) as f:
        json.dump(batteries_json, f, indent=4)


def generate_emulated_battery_csv_file_with_device_id(
        path: str,
        battery_file: str,
        device_file: str,
        num_rows: int,
        batter_brands: str
):

    # get the device id list
    device_df = convert_csv_to_pandas(file=device_file, path=path)
    device_id_list = device_df["device_id"][:num_rows].tolist()

    header = ['device_id', 'device_name',
              'battery_token', 'battery_sn', 'device_brand']
    if len(device_id_list) < num_rows:
        raise Exception("device_id_list is not enough")
    # Generate data for each row
    rows = []
    for i in range(num_rows):
        row = [
            device_id_list[i],
            "battery_" + str(i),
            guid(),  # Generate random UUID v4 for battery_token
            # Generate 5-digit random number for battery_sn
            str(random.randint(10000, 99999)),
            batter_brands  # Set device_brand to "Tesla"
        ]
        rows.append(row)
    saved_battery_csv_file = os.path.join(path, battery_file)
    if not os.path.exists(path):
        os.makedirs(path)
    # Write the data to a CSV file
    with open(saved_battery_csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)


def convert_csv_to_pandas(file: str, path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns a pandas dataframe.

    Parameters:
    filepath (str): The path of the CSV file to be read.

    Returns:
    pd.DataFrame: The pandas dataframe containing the data from the CSV file.
    """
    filepath = os.path.join(path, file)
    if not os.path.exists(filepath):
        print(filepath)
        raise Exception("csv file path does not exist")
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise Exception(f"Error when reading csv file: {e}")
    return df


def make_command_list(
    market_resources_dict_list: List[Dict],
    resouce_agent_dict_list: List[Dict],
    agent_device_dict_list: List[Dict],
    battery_token_df: pd.DataFrame,
    market_interval_in_second: str

) -> List[Dict]:
    """
    the output comnnad list should be like this
    {
        "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
        "resource_id": "caff6719c24359a155a4d0d2f265a7",
        "market_interval_in_second": "300",
        flexible: true,
        "meter_id": "6436a67e184d3694a15886215ae464"
        "devices": [
            {
                "device_id": "807f8e4a37446e80c5756a74a3598d",
                "device_name": "battery_0",
                "device_type": "ES",
                "device_settings": {
                    "battery_token": "12321321qsd",
                    "battery_sn": "66354",
                    "device_brand": "SONNEN_BATTERY"
                },

            }
        ]
    }
    """
    command_list = list()
    for agent in agent_device_dict_list:

        agent_id = agent['agent_id']
        device_ids = agent['device_ids']
        resource_id = None
        market_id = None
        for resource_agent in resouce_agent_dict_list:
            if agent_id in resource_agent['agent_ids']:
                resource_id = resource_agent['resource_id']
                break
        for market_resource in market_resources_dict_list:
            if resource_id in market_resource['resource_ids']:
                market_id = market_resource['market_id']
                break

        command = {
            AGNET_KEY.AGENT_ID.value: agent_id,
            AGNET_KEY.RESOURCE_ID.value: resource_id,
            AGNET_KEY.MARKET_INTERVAL_IN_SECOND.value: market_interval_in_second,
            AGNET_KEY.DEVICES.value: [{
                DEVICES_KEY.DEVICE_ID.value: device_id,
                DEVICES_KEY.DEVICE_NAME.value: "battery_" + str(i),
                DEVICES_KEY.DEVICE_TYPE.value: "ES",
                DEVICES_KEY.FLEXIBLE.value: True,
                DEVICES_KEY.METER_ID.value: guid(),  # TODO: need to be changed
                DEVICES_KEY.DEVICE_SETTINGS.value: {
                    DEVICE_SETTING_KEY.BATTERY_TOKEN.value: battery_token_df[battery_token_df['device_id'] == device_id]['battery_token'].values[0],
                    DEVICE_SETTING_KEY.BATTEY_SN.value: str(battery_token_df[battery_token_df['device_id'] == device_id]['battery_sn'].values[0]),
                    DEVICE_SETTING_KEY.BATTERY_BRANDS.value: battery_token_df[
                        battery_token_df['device_id'] == device_id]['device_brand'].values[0]
                }
            }for i, device_id in enumerate(device_ids)
            ]}
        command_list.append(command)
    return command_list

# create function to


def get_meter_device_relation(
    meters_table_df: pd.DataFrame,
    device_id_list=List[str],
):
    meter_device_dict_list = []
    meter_id_list = []

    filter_meter_df = meters_table_df[meters_table_df['device_id'].isin(
        device_id_list)].reset_index(drop=True)
    print(filter_meter_df.head(5))
    return meter_device_dict_list, meter_id_list


def get_agent_device_relation(
    devices_table_df: pd.DataFrame,
    agent_id_list: List[str],
    device_type: str,


) -> Tuple[List[Dict], List[str]]:

    filter_devices_df = devices_table_df[devices_table_df['agent_id'].isin(
        agent_id_list)].reset_index(drop=True)
    agent_device_dict_list = []
    device_id_list = []
    for agent_id in agent_id_list:
        # for device_type in device_types:
        device_ids = filter_devices_df[

            (filter_devices_df['agent_id'] == agent_id) &
            (filter_devices_df['device_type'] == device_type)

        ]['device_id'].unique()
        device_id_list.extend(device_ids)

        agent_device_dict_list.append({
            #
            "agent_id": agent_id, "device_ids": [device_id for device_id in device_ids],

        })
    return agent_device_dict_list, device_id_list


def get_resource_agent_relation(
    agents_table_df: pd.DataFrame,
    resources_ids: List[str],
    number_of_agent_per_resource: int = 1


) -> Tuple[List[Dict], List[str]]:
    filer_resource_df = agents_table_df[agents_table_df['resource_id'].isin(
        resources_ids)].reset_index(drop=True)
    # find the relation between the resource id and the agent id
    agent_id_list = []
    resouce_agent_dict_list = []
    for reource_id in resources_ids:
        agent_ids = filer_resource_df[filer_resource_df['resource_id']
                                      == reource_id]['agent_id'].unique()[: number_of_agent_per_resource]
        resouce_agent_dict_list.append({
            "resource_id": reource_id, "agent_ids": [agent_id for agent_id in agent_ids]
        })
        agent_id_list.extend(agent_ids)
    return resouce_agent_dict_list, agent_id_list


# match the resouce id with the


def get_market_and_resource_ids(
        dataframe: pd.DataFrame,
        number_of_market: int,
        number_of_resouce_per_market: int,
        interval: Market_Interval) -> Tuple[List[Dict], List[str]]:
    # Filter rows where interval is 60
    filtered = dataframe[dataframe['interval'] == interval]

    # Get the first 2 market_ids
    market_ids = filtered['market_id'].unique()[:number_of_market]

    # Get the first 2 resource_ids for each market_id
    market_resources_dict_list = []
    resources_ids = []
    for market_id in market_ids:
        resources = filtered[filtered['market_id'] == market_id]['resource_id'].unique()[
            : number_of_resouce_per_market]
        market_resources_dict_list.append(
            {"market_id": market_id, "resource_ids": [
                resource for resource in resources]}
        )
        resources_ids.extend(resources)
    return market_resources_dict_list, resources_ids
