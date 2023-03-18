
import boto3
import os
import json
import uuid

import time
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from handle_action import handle_action
from models_and_classes.SQSService import SQSService


def worker_app(
        FIFO_SQS_URL: str,
        FIFO_DLQ_URL: str,
        BACKEND_S3_BUCKET_NAME: str,
        DYNAMODB_AGENTS_TABLE_NAME: str,
        AWS_REGION: str
):
    # poll message from a fifo sqs
    process_task_from_fifo_sqs(
        queue_url=FIFO_SQS_URL,
        fifo_dlq_url=FIFO_DLQ_URL,
        BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
        DYNAMODB_AGENTS_TABLE_NAME=DYNAMODB_AGENTS_TABLE_NAME,
        AWS_REGION=AWS_REGION
    )
    return


def validate_message(message: dict) -> bool:
    """
    Validate the message
    """


def process_task_from_fifo_sqs(
    queue_url: str,
    fifo_dlq_url: str,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_TABLE_NAME: str,
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
        except Exception as e:
            print(f"Error in receive_message: {e}")
            # send to dlq
            time.sleep(5)
            continue

        # If no messages, exit loop
        if message is None:
            print("No message received at %s" % str(time.time()))
            time.sleep(5)

        else:
            # Process the message
            start_time_process_time = time.time()

            print('Received message: %s' % message['Body'])

            # Wait for task to finish before pulling next message
            # check the sqs title attribute to see the task action
            if 'MessageAttributes' not in message or 'Action' not in message['MessageAttributes']:
                print("No Action attribute in message")
                print("delete message from queue,send to d")

                dlq_service.send_message(
                    message_body=json.loads(message['Body'])
                )

                sqs_service.delete_message(
                    receipt_handle=message['ReceiptHandle']
                )

                continue
            message_attributes = message['MessageAttributes']
            action = message_attributes['Action']['StringValue']
            message_body = json.loads(message['Body'])

            # delete the message from the queue first to avoid duplicate
            sqs_service.delete_message(
                receipt_handle=message['ReceiptHandle']
            )
            try:
                handle_action(
                    action=action,
                    message_body=message_body,
                    BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
                    DYNAMODB_AGENTS_TABLE_NAME=DYNAMODB_AGENTS_TABLE_NAME,
                    AWS_REGION=AWS_REGION
                )
            except Exception as e:
                dlq_service.send_message(
                    message_body=json.loads(message['Body'])
                )
                print(
                    f"Error in handle_action: {e}: Send out notification to SNS")
            end_process_time = time.time()
            process_time = int(end_process_time - start_time_process_time)
            print(
                f"===action:{action} process time: {str(process_time)}  ====")
            # Delete the message from the queue

            time.sleep(5)
