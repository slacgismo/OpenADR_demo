from typing import Dict
from .guid import guid
import logging
from classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from process_acitons.process_task_from_fifo_sqs import handle_action


def validate_message(message: dict) -> bool:
    """
    Validate the message
    """
    # Todo: validate the message
    if (
        "MessageAttributes" not in message
        or "Action" not in message["MessageAttributes"]
        or "Body" not in message
    ):
        print("No Action, or MessageAttributes, or Body  attribute in message")
        print("delete message from queue,send to d")
        return False

    return True


def simulated_message() -> Dict:
    message_body = {
        "agent_id": guid(),
        "resource_id": guid(),
        "market_interval_in_seconds": "300",
        "market_id": guid(),
        "devices": [
            {
                "device_id": guid(),
                "device_name": "battery_0",
                "device_type": "ES",
                "device_settings": {
                    "battery_token": "12321321qsd",
                    "battery_sn": "66354",
                    "device_brand": "SONNEN_BATTERY",
                },
                "biding_price_threshold": "0.15",
                "meter_id": "6436a67e184d3694a15886215ae464",
            }
        ],
    }
    return message_body


def validate_agent_actions(
    message_body: dict,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
) -> bool:
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
