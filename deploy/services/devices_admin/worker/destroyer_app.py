
import os

from handle_action import handle_action, ECS_ACTIONS_ENUM
from models_and_classes.DynamoDBService import DynamoDBService


def destroyer_app(
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_TABLE_NAME: str,
    AWS_REGION: str
):
    # emulate the sqs message body in oder we need the controller_app to polulate the message body in the future
    # when wee have mulitple destroyers
    # first list all the agents in the dynamodb
    dynamodb_service = DynamoDBService(table_name=DYNAMODB_AGENTS_TABLE_NAME)
    agents = dynamodb_service.list_all_items_primary_id(primary_id="agent_id")
    for agent in agents:
        print(agent)
    # handle_action(
    #     action=ECS_ACTIONS_ENUM.DELETE.value,
    #     message_body=message_body,
    #     BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
    #     DYNAMODB_AGENTS_TABLE_NAME=DYNAMODB_AGENTS_TABLE_NAME,
    #     AWS_REGION=AWS_REGION
    # )
    return


# {"agent_id": "00ccff430c4bcfa1f1186f488b88fc", "resource_id": "caff6719c24359a155a4d0d2f265a7", "market_interval_in_second": "300", "devices": [{"device_id": "807f8e4a37446e80c5756a74a3598d", "device_name": "battery_0", "device_type": "HS", "device_params": {"battery_token": "12321321qsd", "battery_sn": "66354", "device_brand": "SONNEN_BATTERY"}, "biding_price_threshold": "0.15", "meter_id": "6436a67e184d3694a15886215ae464"}]}
