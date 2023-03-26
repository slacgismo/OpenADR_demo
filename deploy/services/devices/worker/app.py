"""
This worker is responsible for handling the actions to create the ECS(agent) services
on ECS cluster. Each ECS service is responsible an agent.
A agent always has a VTN and mulitple vens(a ven is a device).
This worker app execute the terraform scripts to create the ECS services.
The action is triggered by the sqs queue to avoid race condition.
"""
from multiprocessing import Process
import datetime
import multiprocessing
import logging
import asyncio
import os
import json
import time
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from handle_action import handle_action
from models_and_classes.SQSService import SQSService
from models_and_classes.S3Service import S3Service
from models_and_classes.DynamoDBService import DynamoDBService
from models_and_classes.STSService import STSService
from models_and_classes.HttpService import HealthCheckService
from models_and_classes.ECSService import ECSService
from models_and_classes.helper.task_definition_generator import guid
from models_and_classes.ProcessThread import ProcessThread
from typing import Dict
import threading
# from dotenv import load_dotenv
import socketserver
import time
from handle_action import handle_action
# load_dotenv()
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
SQS_GROUPID = os.environ['SQS_GROUPID']
if SQS_GROUPID is None:
    raise Exception("SQS_GROUPID is not set")

ENV = os.environ['ENV']
if ENV is None:
    raise Exception("ENV is not set")

WORKER_PORT = os.environ['WORKER_PORT']
if WORKER_PORT is None:
    raise Exception("WORKER_PORT not set")


FIFO_SQS_URL = os.environ['FIFO_SQS_URL']
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")


BACKEND_S3_BUCKET_NAME = os.environ['BACKEND_S3_BUCKET_NAME']
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")


FIFO_DLQ_URL = os.environ['FIFO_DLQ_URL']
if FIFO_DLQ_URL is None:
    raise Exception("FIFO_DLQ_URL is not set")

AWS_REGION = os.environ['AWS_REGION']
if AWS_REGION is None:
    raise Exception("AWS_REGION is not set")

DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = os.environ[
    'DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME']
if DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is None:
    raise Exception(
        "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is not set")

ECS_CLUSTER_NAME = os.environ['ECS_CLUSTER_NAME']
if ECS_CLUSTER_NAME is None:
    raise Exception("ECS_CLUSTER_NAME is not set")


def validate_message(message: dict) -> bool:
    """
    Validate the message
    """
    # Todo: validate the message
    if 'MessageAttributes' not in message or 'Action' not in message['MessageAttributes'] or 'Body' not in message:
        print("No Action, or MessageAttributes, or Body  attribute in message")
        print("delete message from queue,send to d")
        return False

    return True


def process_task_from_fifo_sqs(
    queue_url: str,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
    ENV: str,
    MaxNumberOfMessages: int = 1,
        WaitTimeSeconds: int = 10,
        VisibilityTimeout: int = 20):
    """
    Process the task from the fifo sqs queue
    params: queue_url: str
    params: BACKEND_S3_BUCKET_NAME: str
    params: DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str
    params: AWS_REGION: str
    params: MaxNumberOfMessages: int = 1
    params: WaitTimeSeconds: int = 10
    params: VisibilityTimeout: int = 20
    return: None
    """
    logging.info("Start the worker app")
    while True:
        time.sleep(2)
        try:
            # TODO: add dlq if we need it

            sqs_service = SQSService(
                queue_url=queue_url
            )
            # try:
            message = sqs_service.receive_message(
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout,
                group_id=SQS_GROUPID
            )
            # except Exception as e:
            #     raise logging.error(f"receive_message error : {e}")

            if message is None:
                logging.info("Waiting.... %s" %
                             str(int(time.time())))
                continue

            sqs_service.delete_message(
                receipt_handle=message['ReceiptHandle']
            )
            if validate_message(message) is False:
                raise Exception("Invalid message received")

            else:

                # Process the message
                start_time_process_time = time.time()

                logging.info('Received message: %s' % message['Body'])
                message_attributes = message['MessageAttributes']
                action = message_attributes['Action']['StringValue']
                message_body = json.loads(message['Body'])
                print("======== ")
                # delete the message from the queue first to avoid duplicate
                handle_action(
                    action=action,
                    message_body=message_body,
                    BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
                    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
                    AWS_REGION=AWS_REGION,
                )
                end_process_time = time.time()
                process_time = int(end_process_time - start_time_process_time)
                time.sleep(5)
                logging.info(
                    f"===action:{action} process time: {str(process_time)}  ====")
                # Delete the message from the queue
        except Exception as e:
            logging.error(f"Error : {e}")


def simulated_message() -> Dict:
    message_body = {
        "agent_id": guid(),
        "resource_id": guid(),
        "market_interval_in_second": "300",
        "market_id": guid(),
        "devices": [
            {
                "device_id": guid(),
                "device_name": "battery_0",
                "device_type": "ES",
                "device_params": {
                    "battery_token": "12321321qsd",
                    "battery_sn": "66354",
                    "device_brand": "SONNEN_BATTERY"
                },
                "biding_price_threshold": "0.15",
                "meter_id": "6436a67e184d3694a15886215ae464"
            }
        ]}
    return message_body


def validate_agent_actions(message_body: dict) -> bool:
    """
    Validate the message
    """
    try:
        # create a emulate sqs message

        logging.info("Start to create a validate agent")
        handle_action(
            action=ECS_ACTIONS_ENUM.CREATE.value,
            message_body=message_body,
            BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            AWS_REGION=AWS_REGION,
        )
        logging.info("Start to update a validate agent")
        handle_action(
            action=ECS_ACTIONS_ENUM.UPDATE.value,
            message_body=message_body,
            BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            AWS_REGION=AWS_REGION,
        )
        logging.info("Start to delete a validate agent")
        handle_action(
            action=ECS_ACTIONS_ENUM.DELETE.value,
            message_body=message_body,
            BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            AWS_REGION=AWS_REGION,
        )
        logging.info("End to validate create/update/delete agent")
    except Exception as e:
        raise logging.error(f"Validate create/delete/update error : {e}")


def main():
    """
    Main function
    """
    # process_task_from_fifo_sqs(
    #     queue_url=FIFO_SQS_URL,
    #     BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
    #     DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
    #     AWS_REGION=AWS_REGION,
    #     ENV=ENV,
    # )
    http_server = HealthCheckService(
        host="localhost", port=8070, path="/health")
    http_server.run(
        long_process_fn=process_task_from_fifo_sqs, long_process_args=(
            FIFO_SQS_URL,
            BACKEND_S3_BUCKET_NAME,
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            AWS_REGION,
            ENV,
        )
    )


if __name__ == '__main__':
    main()
