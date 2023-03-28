
"""
This CLI app is responsible for handling the actions to control the worker app.
It create/update/delete sqs message command to control the worker app.
Once worker app receive the sqs message, it will handle the action.
"""


import os
import uuid
from enum import Enum
import pandas as pd
import random
import click

from models_and_classes.create_agents import generate_first_number_agents_from_simulation_csv_file, Market_Interval, Device_Type, generate_emulated_battery_csv_file_with_device_id, BATTERY_BRANDS, ECS_ACTIONS_ENUM
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

except Exception as e:
    raise Exception(f"ENV is not set correctly: {e}")

# Parent Command


class Envoriment(Enum):
    DEV = "DEV"
    PROD = "PROD"
    LOCAL = "LOCAL"


@click.group()
def cli():
    pass

# ***************************
#  Generate battery files
# ***************************


@click.command()
def create_battery_file():

    generate_emulated_battery_csv_file_with_device_id(
        path="./simulation_data_files",
        battery_file="simluated_battery.csv",
        device_file="dump_devices.csv",
        num_rows=500,
        batter_brands=BATTERY_BRANDS.SONNEN_BATTERY.value,
    )

# ***************************
#  Generate message sqs and send to sqs queue
# ***************************


@click.command()
def create_agents():
    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=2,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,
        ecs_action=ECS_ACTIONS_ENUM.CREATE.value,
        ENV=ENV,
        SQS_GROUPID=SQS_GROUPID

    )


@click.command()
def update_agents():
    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=2,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,
        ecs_action=ECS_ACTIONS_ENUM.UPDATE.value,
        ENV=ENV,
        SQS_GROUPID=SQS_GROUPID
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
    # generate_first_number_agents_from_simulation_csv_file(
    #     market_interval=Market_Interval.One_Minute.value,
    #     number_of_market=1,
    #     number_of_resouce_per_market=1,
    #     number_of_agent_per_resource=10,
    #     device_type=Device_Type.ES.value,
    #     fifo_sqs=FIFO_SQS_URL,
    #     ecs_action=ECS_ACTIONS_ENUM.DELETE.value
    # )


# add the command to the cli
cli.add_command(create_battery_file)
cli.add_command(create_agents)
cli.add_command(destroy_all_agents)
cli.add_command(update_agents)

if __name__ == '__main__':
    cli()
