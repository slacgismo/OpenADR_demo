"""
This worker is responsible for handling the actions to create the ECS(agent) services 
on ECS cluster. Each ECS service is responsible an agent. 
A agent always has a VTN and mulitple vens(a ven is a device).
This worker app execute the terraform scripts to create the ECS services.
The action is triggered by the sqs queue to avoid race condition.
"""

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
from models_and_classes.HTTPServer import HTTPServer
from models_and_classes.ECSService import ECSService
# from dotenv import load_dotenv
import socketserver
import time
from handle_action import handle_action
# load_dotenv()
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

logging.info(f"Start the worker app")

HEALTH_CHEKC_PORT = os.environ['HEALTH_CHEKC_PORT']
if HEALTH_CHEKC_PORT is None:
    raise Exception("health_check_port not set")


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
        try:
            # TODO: add dlq if we need it

            sqs_service = SQSService(
                queue_url=queue_url
            )
            try:
                message = sqs_service.receive_message(
                    MaxNumberOfMessages=MaxNumberOfMessages,
                    WaitTimeSeconds=WaitTimeSeconds,
                    VisibilityTimeout=VisibilityTimeout
                )
            except Exception as e:
                raise logging.error(f"Error : {e}")

            if message is None:
                logging.info("Waiting.... %s" %
                             str(int(time.time())))
                time.sleep(2)
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

        time.sleep(2)


def main():
    """
    Main function
    """
    # validate the permissions
    # valudate s3 bucket
    try:
        sts_service = STSService()
        s3_service = S3Service(
            bucket_name=BACKEND_S3_BUCKET_NAME
        )
        s3_service.validate_s3_bucket(
            sts_service=sts_service
        )
        # validate the dynamodb table
        dynamodb_service = DynamoDBService(
            table_name=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME
        )
        dynamodb_service.list_number_of_items()

        # validate the sqs queue
        sqs_service = SQSService(
            queue_url=FIFO_SQS_URL
        )
        sqs_message = sqs_service.receive_message(
            MaxNumberOfMessages=1,
            WaitTimeSeconds=2,
            VisibilityTimeout=2
        )
        logging.info("Validate the sqs queue")
        # validate the dlq
        dlq_service = SQSService(
            queue_url=FIFO_DLQ_URL
        )
        dlq_message = dlq_service.receive_message(
            MaxNumberOfMessages=1,
            WaitTimeSeconds=2,
            VisibilityTimeout=2
        )
        logging.info("Validate the dlq queue")
        # validate ecs
        ecs_service = ECSService(
            ecs_cluster_name=ECS_CLUSTER_NAME
        )
        active_services = ecs_service.list_ecs_services()
        logging.info("Validate the ecs cluster")
    except Exception as e:
        raise logging.error(f"Validate permission error : {e}")

    process_task_from_fifo_sqs(
        queue_url=FIFO_SQS_URL,
        BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        AWS_REGION=AWS_REGION
    )


if __name__ == '__main__':
    main()


# Run the client in the Python AsyncIO Event Loop

# asyncio.run(main())  # main loop
