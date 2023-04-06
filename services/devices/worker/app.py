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
SQS_GROUPID = os.environ.get("SQS_GROUPID")
if SQS_GROUPID is None:
    raise Exception("SQS_GROUPID is not set")
logging.info(f"sqs group id is {SQS_GROUPID}")

ENV = os.environ.get("ENV")
if ENV is None:
    raise Exception("ENV is not set")
logging.info(f"ENV  is {ENV}")
WORKER_PORT = os.environ.get("WORKER_PORT")
if WORKER_PORT is None:
    raise Exception("WORKER_PORT not set")
logging.info(f"worker port is {WORKER_PORT}")

FIFO_SQS_URL = os.environ.get("FIFO_SQS_URL")
logging.info(f"FIFO_SQS_URL is {FIFO_SQS_URL}")
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")


BACKEND_S3_BUCKET_NAME = os.environ.get("BACKEND_S3_BUCKET_NAME")
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")


FIFO_DLQ_URL = os.environ.get("FIFO_DLQ_URL")
if FIFO_DLQ_URL is None:
    raise Exception("FIFO_DLQ_URL is not set")

AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
if AWS_DEFAULT_REGION is None:
    raise Exception("AWS_REGION is not set")

DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = os.environ.get(
    "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME"
)
if DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is None:
    raise Exception(
        "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is not set")

ECS_CLUSTER_NAME = os.environ.get("ECS_CLUSTER_NAME")
if ECS_CLUSTER_NAME is None:
    raise Exception("ECS_CLUSTER_NAME is not set")


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
            ENV,
            SQS_GROUPID,
        ),
    )


if __name__ == "__main__":
    main()
