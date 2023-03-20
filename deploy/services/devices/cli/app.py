
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
from dotenv import load_dotenv
load_dotenv()
""""
This controller app is used to control the worker app for developement and testing purpose.
It will generate following sqs:
1. generate number agents for test purpose
2. destroy number agents

"""

FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")

ECS_CLUSTER_NAME = os.getenv('ecs_cluster_name')
if ECS_CLUSTER_NAME is None:
    raise Exception("ECS_CLUSTER_NAME is not set")
# create funtion to read csv file and convert to json forma


# Parent Command
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
        ecs_action=ECS_ACTIONS_ENUM.CREATE.value

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
        ecs_action=ECS_ACTIONS_ENUM.UPDATE.value
    )
# ***************************
#  Destroy all workers
# ***************************


@click.command()
def destroy_all_agents(
):
    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=2,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,
        ecs_action=ECS_ACTIONS_ENUM.DELETE.value
    )


# add the command to the cli
cli.add_command(create_battery_file)
cli.add_command(create_agents)
cli.add_command(destroy_all_agents)
cli.add_command(update_agents)

if __name__ == '__main__':
    cli()
