
import boto3
import os
import json
import uuid

import time
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from handle_action import handle_action
from enum import Enum
from destroyer_app import destroyer_app
from controller_app import controller_app
from test_app import test_app
from worker_app import worker_app


class WORKER_TYPES(Enum):
    WORKER = "WORKER"
    DESTROYER = "DESTROYER"
    CONTROLLER = "CONTROLLER"
    TEST = "TEST"


FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")
BACKEND_S3_BUCKET_NAME = os.getenv('backend_s3_bucket_devices_admin')
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")

DYNAMODB_AGENTS_TABLE_NAME = os.getenv('dynamodb_agents_table_name')
if DYNAMODB_AGENTS_TABLE_NAME is None:
    raise Exception("DYNAMODB_AGENTS_TABLE_NAME is not set")

FIFO_DLQ_URL = os.getenv('openadr_workers_dlq_url')
if FIFO_DLQ_URL is None:
    raise Exception("FIFO_DLQ_URL is not set")

AWS_REGION = os.getenv('aws_region')
if AWS_REGION is None:
    raise Exception("AWS_REGION is not set")

WORKER_TYPE = os.getenv('worker_type')
if WORKER_TYPE is None:
    raise Exception("WORKER_TYPE is not set")
if WORKER_TYPE not in [WORKER_TYPES.WORKER.value, WORKER_TYPES.DESTROYER.value]:
    raise Exception("WORKER_TYPE is not valid")

# Select the table
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


if __name__ == '__main__':
    # poll message from a fifo sqs
    if WORKER_TYPE == WORKER_TYPES.WORKER.value:
        # regural worker to generate ecs service. It take command from fifo sqs
        worker_app(
            FIFO_SQS_URL=FIFO_SQS_URL,
            FIFO_DLQ_URL=FIFO_DLQ_URL,
            BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_TABLE_NAME=DYNAMODB_AGENTS_TABLE_NAME,
            AWS_REGION=AWS_REGION
        )

    elif WORKER_TYPE == WORKER_TYPES.DESTROYER.value:
        # destroy all ecs service. It's trigger by main terrafrom destroy command
        destroyer_app()
    elif WORKER_TYPE == WORKER_TYPES.CONTROLLER.value:
        # generate sqs for test app or destroyer app
        controller_app()
    elif WORKER_TYPE == WORKER_TYPES.TEST.value:
        # test ecs create/delete/update
        test_app()
    else:
        raise Exception("WORKER_TYPE is not valid")
