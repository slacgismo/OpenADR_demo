
"""
This CLI app is responsible for handling the actions to control the worker app.
It create/update/delete sqs message command to control the worker app.
Once worker app receive the sqs message, it will handle the action.
"""

import datetime
import os
import uuid
from enum import Enum
import pandas as pd
import random
import click
from models_and_classes.create_json_file_from_csv import filter_and_convert_csv_to_json
from models_and_classes.create_agents import generate_first_number_agents_from_simulation_csv_file, Market_Interval, Device_Type,  BATTERY_BRANDS, ECS_ACTIONS_ENUM
from models_and_classes.destroy_agents import destroy_all
import logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

logging.info(f"Start the worker app")

""""
This controller app is used to control the worker app for developement and testing purpose.
It will generate following sqs:
1. generate number agents for test purpose
2. destroy number agents

"""
try:
    # The SQS_GROUPID is used to separate the sqs queue for different environment.
    # if you want to send message to AWS worker, the SQS_GROUPID should be set to "AWS"
    # if you want to send message to local worker, the SQS_GROUPID should be set to "LOCAL"
    SQS_GROUPID = os.environ['SQS_GROUPID']
    ENV = os.environ['ENV']
    FIFO_SQS_URL = os.environ['FIFO_SQS_URL']
    ECS_CLUSTER_NAME = os.environ['ECS_CLUSTER_NAME']
    # create funtion to read csv file and convert to json forma
    BACKEND_S3_BUCKET_NAME = os.environ['BACKEND_S3_BUCKET_NAME']
    MARKET_START_TIME = os.environ['MARKET_START_TIME']

except Exception as e:
    raise Exception(f"ENV is not set correctly: {e}")

# Parent Command


class Envoriment(Enum):
    DEV = "DEV"
    PROD = "PROD"
    LOCAL = "LOCAL"


def convert_datetime_to_timsestamp(time_str: str, format: str = "%Y-%m-%d %H:%M %Z") -> int:
    time_format = "%Y-%m-%d %H:%M %Z"
    # convert datetime object to timestamp
    dt = datetime.datetime.strptime(time_str, time_format)
    market_start_timestamp = dt.timestamp()
    return int(market_start_timestamp)


@click.group()
def cli():
    pass

# ***************************
#  Generate battery files
# ***************************


@click.command()
def create_db_json():
    filter_and_convert_csv_to_json(
        devices_type=[Device_Type.ES.value],
        num_rows=100,
        path="./simulation_data_files",
        battery_file="simluated_battery.csv",
        batter_brands=BATTERY_BRANDS.SONNEN_BATTERY.value,
    )
    pass
    # generate_emulated_battery_csv_file_with_device_id(
    #     path="./simulation_data_files",
    #     battery_file="simluated_battery.csv",
    #     device_file="dump_devices.csv",
    #     num_rows=500,
    #     batter_brands=BATTERY_BRANDS.SONNEN_BATTERY.value,
    # )
    # parse the csv file to json file
    # export devices
    # parse_csv_and_export_json_file(
    #     csv_file_path="./simulation_data_files/dump_devices.csv",
    #     json_file_path="./simulation_data_files/dump_devices.json",
    # )
    # # export orders
    # parse_csv_and_export_json_file(
    #     csv_file_path="./simulation_data_files/dump_orders.csv",
    #     json_file_path="./simulation_data_files/dump_orders.json",
    # )
    # # export dispatches
    # parse_csv_and_export_json_file(
    #     csv_file_path="./simulation_data_files/dump_dispatches.csv",
    #     json_file_path="./simulation_data_files/dump_dispatches.json",
    # )

    # parse_batteries_csv_file_to_json(
    #     path="./simulation_data_files",
    #     battery_file="simluated_battery.csv",
    #     num_rows=250,
    #     batter_brands=BATTERY_BRANDS.SONNEN_BATTERY.value,
    # )

    # ***************************
    #  Generate message sqs and send to sqs queue
    # ***************************


@click.command()
def create_agents():

    time_format = "%Y-%m-%d %H:%M %Z"

    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=MARKET_START_TIME, format=time_format
    )

    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=1,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,
        ecs_action=ECS_ACTIONS_ENUM.CREATE.value,
        ENV=ENV,
        SQS_GROUPID=SQS_GROUPID,
        market_start_timestamp=market_start_timestamp)


@click.command()
def update_agents():
    time_format = "%Y-%m-%d %H:%M %Z"

    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=MARKET_START_TIME, format=time_format
    )
    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=2,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,
        ecs_action=ECS_ACTIONS_ENUM.UPDATE.value,
        ENV=ENV,
        SQS_GROUPID=SQS_GROUPID,
        market_start_timestamp=market_start_timestamp
    )
# ***************************
#  Destroy all workers
# ***************************


@click.command()
def destroy_all_agents(
):
    destroy_all(
        fifo_sqs=FIFO_SQS_URL,
        ecs_cluster_name=ECS_CLUSTER_NAME,
        group_id=SQS_GROUPID
    )


# add the command to the cli
cli.add_command(create_db_json)
cli.add_command(create_agents)
cli.add_command(destroy_all_agents)
cli.add_command(update_agents)

if __name__ == '__main__':
    cli()
