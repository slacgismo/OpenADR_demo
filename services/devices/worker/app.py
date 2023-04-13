"""
This worker is responsible for handling the actions to create the ECS(agent) services
on ECS cluster. Each ECS service is responsible an agent.
A agent always has a VTN and mulitple vens(a ven is a device).
This worker app execute the terraform scripts to create the ECS services.
The action is triggered by the sqs queue to avoid race condition.
"""

import logging

import os

from classes.HttpService import HealthCheckService
from typing import Dict

# from dotenv import load_dotenv

from process_acitons.process_task_from_fifo_sqs import process_task_from_fifo_sqs

# load_dotenv()
logging.basicConfig(
    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO
)

try:

    ENVIRONMENT = os.environ['ENVIRONMENT']
    FIFO_SQS_URL = os.environ['FIFO_SQS_URL']
    BACKEND_S3_BUCKET_NAME = os.environ['BACKEND_S3_BUCKET_NAME']
    AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = os.environ[
        "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME"]
    ECS_CLUSTER_NAME = os.environ['ECS_CLUSTER_NAME']
    METER_API_URL = os.environ['METER_API_URL']
    DEVICES_API_URL = os.environ['DEVICES_API_URL']
    ORDERS_API_URL = os.environ['ORDERS_API_URL']
    DISPATCHES_API_URL = os.environ['DISPATCHES_API_URL']
    EMULATED_DEVICE_API_URL = os.environ['EMULATED_DEVICE_API_URL']
except Exception as e:
    raise Exception(f"Error in parise environment variables {e}")

# CONSTANTS
WORKER_PORT = "8000"


def main():
    """
    Main function
    """

    http_server = HealthCheckService(
        host="localhost", port=int(WORKER_PORT), path="/health"
    )
    http_server.run(
        long_process_fn=process_task_from_fifo_sqs,
        long_process_args=(
            FIFO_SQS_URL,
            BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            AWS_DEFAULT_REGION,
            ENVIRONMENT,
            METER_API_URL,
            DEVICES_API_URL,
            ORDERS_API_URL,
            DISPATCHES_API_URL,
            EMULATED_DEVICE_API_URL,
        ),
    )


if __name__ == "__main__":
    main()
