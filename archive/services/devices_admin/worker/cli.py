
import boto3
import os
import uuid
from enum import Enum
import pandas as pd
import random
import click
from models_and_classes.create_workers import generate_first_number_agents_from_simulation_csv_file, Market_Interval, Device_Type, generate_emulated_battery_csv_file_with_device_id, BATTERY_BRANDS
from models_and_classes.destroy_workers import destroy_workers

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
def create_workers():
    generate_first_number_agents_from_simulation_csv_file(
        market_interval=Market_Interval.One_Minute.value,
        number_of_market=1,
        number_of_resouce_per_market=1,
        number_of_agent_per_resource=2,
        device_type=Device_Type.ES.value,
        fifo_sqs=FIFO_SQS_URL,

    )
# ***************************
#  Destroy all workers
# ***************************


@click.command()
@click.option(
    "--number",
    "-n",
    help="Destroy number of workers, if 0 destroy all worker",
    default=0,
)
def destroy(
    number: int = 0
):
    destroy_workers(
        number_of_workers=number,
        ecs_cluster_name=ECS_CLUSTER_NAME
    )


# add the command to the cli
cli.add_command(create_battery_file)
cli.add_command(create_workers)
cli.add_command(destroy)


if __name__ == '__main__':
    cli()
