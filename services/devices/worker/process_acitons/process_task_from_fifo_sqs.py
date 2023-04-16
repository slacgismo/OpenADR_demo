from classes.SQSService import SQSService
import time
import logging
from .handle_action import handle_action
import json
from enum import Enum


class MessageBodyKeys(Enum):
    EVENTNAME = "eventName"
    AGENT_ID = "agent_id"
    RESOURCE_ID = "resource_id"
    MARKET_INTERVAL_IN_SECONDS = "market_interval_in_seconds"
    DEVICE_ID = "device_id"
    DEVICE_TYPE = "device_type"
    METER_ID = "meter_id"
    DEVICE_SETTINGS = "device_settings"
    PRICE_FLOOR = "price_floor"
    PRICE_CEILING = "price_ceiling"


class DeviceSettingsKeys(Enum):
    BATTERY_TOKEN = "battery_token"
    BATTERY_SN = "battery_sn"
    DEVICE_BRAND = "device_brand"
    IS_USING_MOCK_DEVICE = "is_using_mock_device"
    FLEXIBLE = "flexible"


def process_task_from_fifo_sqs(
    queue_url: str,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
    ENVIRONMENT: str,
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
            MaxNumberOfMessages = 1
            WaitTimeSeconds = 5
            VisibilityTimeout = 10
            message = sqs_service.receive_message(
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout,
                group_id=ENVIRONMENT,
            )
            if message is None:
                logging.info("Waiting.... %s" % str(int(time.time())))
                continue

            else:
                # Process the message
                start_time_process_time = time.time()

                logging.info("Received message: %s" % message["Body"])

                # action = message_attributes["Action"]["StringValue"]
                message_body = json.loads(message["Body"])

                if validate_message_body(message_body) is False:
                    raise Exception("Invalid message body received")

                action = message_body["eventName"]
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


def validate_message_body(message_body: dict) -> bool:
    """
    Validate the message body
    params: message_body: dict
    return: bool
    """
    for key in MessageBodyKeys:
        if key.value not in message_body:
            logging.error(f"Missing key: {key.value}")
            return False
        # Validate the device settings
        if key.value == MessageBodyKeys.DEVICE_SETTINGS.value:
            device_settings = message_body[key.value]
            for device_setting_key in DeviceSettingsKeys:
                if device_setting_key.value not in device_settings:
                    logging.error(f"Missing key: {device_setting_key.value}")
                    return False
    return True
