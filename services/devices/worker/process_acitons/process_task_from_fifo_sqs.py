from classes.SQSService import SQSService
import time
import logging
from .handle_action import handle_action
from .validation import validate_message
import json


def process_task_from_fifo_sqs(
    queue_url: str,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
    ENV: str,
    SQS_GROUPID: str,
    MaxNumberOfMessages: int = 1,
    WaitTimeSeconds: int = 5,
    VisibilityTimeout: int = 5,
):
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

            sqs_service = SQSService(queue_url=queue_url)
            # try:
            message = sqs_service.receive_message(
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout,
                group_id=SQS_GROUPID,
            )
            if message is None:
                logging.info("Waiting.... %s" % str(int(time.time())))
                continue

            if validate_message(message) is False:
                raise Exception("Invalid message received")

            else:
                # Process the message
                start_time_process_time = time.time()

                logging.info("Received message: %s" % message["Body"])
                message_attributes = message["MessageAttributes"]
                action = message_attributes["Action"]["StringValue"]
                message_body = json.loads(message["Body"])

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
                    f"===action:{action} process time: {str(process_time)}  ===="
                )
                # Delete the message from the queue
        except Exception as e:
            logging.error(f"Error : {e}")
