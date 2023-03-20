

import os
import json
# {"agent_id": "195728adee3af42120c157833a391249", "resource_id": "3b4a58e3cd70cd9c6f781d9267c6c5c0", "market_interval_in_second": "60", "market_id": "e64453a9304b51b1c66ce462e2c80c", "devices": [{"device_id": "3bd3c653deee0956613cb09229e5e52a", "device_name": "battery_0", "device_type": "ES", "device_params": {"battery_token": "322302bd7841beac7c407961cdec37", "battery_sn": "76097", "device_brand": "SONNEN_BATTERY"}, "biding_price_threshold":" 8.090370001385232", "meter_id": "2d8f00e2be4e4ca7a94ba3b88da76b"}]}

import time
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from handle_action import handle_action
from models_and_classes.SQSService import SQSService


import time
from handle_action import handle_action


FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")
BACKEND_S3_BUCKET_NAME = os.getenv('backend_s3_bucket_devices_admin')
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")


FIFO_DLQ_URL = os.getenv('openadr_workers_dlq_url')
if FIFO_DLQ_URL is None:
    raise Exception("FIFO_DLQ_URL is not set")

AWS_REGION = os.getenv('aws_region')
if AWS_REGION is None:
    raise Exception("AWS_REGION is not set")

DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = os.getenv(
    'dynamodb_agents_shared_remote_state_lock_table_name')
if DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is None:
    raise Exception(
        "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is not set")


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
    fifo_dlq_url: str,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
    MaxNumberOfMessages: int = 1,
        WaitTimeSeconds: int = 5,
        VisibilityTimeout: int = 5):
    while True:
        try:
            dlq_service = SQSService(
                queue_url=fifo_dlq_url
            )
            sqs_service = SQSService(
                queue_url=queue_url
            )
            message = sqs_service.receive_message(
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout
            )

            if message is None:
                print("No message received at %s" % str(int(time.time())))
                time.sleep(5)
                continue

            sqs_service.delete_message(
                receipt_handle=message['ReceiptHandle']
            )
            if validate_message(message) is False:
                raise Exception("Invalid message received")

            else:

                # Process the message
                start_time_process_time = time.time()

                print('Received message: %s' % message['Body'])
                message_attributes = message['MessageAttributes']
                action = message_attributes['Action']['StringValue']
                message_body = json.loads(message['Body'])

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
                print(
                    f"===action:{action} process time: {str(process_time)}  ====")
                # Delete the message from the queue
                time.sleep(5)
        except Exception as e:
            print(f"Error : {e}")
            # send to dlq
            # dlq_service.send_message(
            #     message_body=json.loads(message['Body'])
            # )

            continue
        time.sleep(5)
        # If no messages, exit loop


if __name__ == '__main__':
    # poll message from a fifo sqs
    process_task_from_fifo_sqs(
        queue_url=FIFO_SQS_URL,
        fifo_dlq_url=FIFO_DLQ_URL,
        BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        AWS_REGION=AWS_REGION
    )
