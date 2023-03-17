from flask import Flask, jsonify, request
import json

import boto3
import os
import uuid
from enum import Enum


ENV = os.getenv('ENV')
ECS_CLUSTER_NAME = os.getenv('ECS_CLUSTER_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
SQS_URL = os.getenv('SQS_URL')
PRIVATE_SG_NAME = os.getenv('PRIVATE_SG_NAME')
ECS_TASK_EXECUTION_ROLE_NAME = os.getenv('ECS_TASK_EXECUTION_ROLE_NAME')
ECS_TASK_ROLE_NAME = os.getenv('ECS_TASK_ROLE_NAME')
PRIVATE_VPC_ID = os.getenv('PRIVATE_VPC_ID')
CLOUDWATCH_NAME = os.getenv('CLOUDWATCH_NAME')
AGENT_ID = os.getenv('AGENT_ID')
# DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

dynamodb = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')
# Select the table
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)


class ECA_ACTIONS(Enum):
    CREATE = "CREATE"
    READ = "READ"
    DELETE = "DELETE"
    UPDATE = "UPDATE"


# Define the item to be created


app = Flask(__name__)

# Dummy data to simulate a database
agents = [
    {"agent_id": "195728adee3af42120c157833a391249",
        "resource_id": "3b4a58e3cd70cd9c6f781d9267c6c5c0", "valid_at": "1678118400"},
    {"agent_id": "37e675944fd7bffd61d761a55ab51433",
        "resource_id": "3b4a58e3cd70cd9c6f781d9267c6c5c0", "valid_at": "1678118400"},

]

openadr_agents_table = [
    {"agent_id": "195728adee3af42120c157833a391249",
        "vtn_id": "d1bd006f-62c0-4ca6-9993-1c892fc92ae4",
        "ven_ids": [
            {
                "ven_id": "b88db86c-45d1-4b54-9580-6885a4c1e5c3",
                "device_id": "72510234-8f7c-4764-a724-35caba626a91",
                "meter_id": "5ad413f3-948d-4ead-a8ea-ffbccb454168",
                "valid_at": "1678118400"
            }

        ],
     "valid_at": "1678118400"},
]

devices = [
    {"device_id": "3bd3c653deee0956613cb09229e5e52a",
        "agent_id": "195728adee3af42120c157833a391249", "device_type": "ES", "valid_at": "1678118400"},
    {"device_id": "320d141048c23741139cc30262369a86",
        "agent_id": "37e675944fd7bffd61d761a55ab51433", "device_type": "ES", "valid_at": "1678118400"}
]
next_id = 4


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


def generate_empty_ecs_services_params(agent_id: str) -> dict:
    params = dict()
    params['agent_id'] = agent_id

    return params


def generate_ecs_services_param_with_devices(agent_id: str, device_ids: list) -> dict:
    params = dict()
    params['agent_id'] = agent_id
    params['agent_id'] = agent_id
    params['device_ids'] = device_ids
    return params


async def check_agent_id_exist(agent_id: str, table_name: str) -> bool:
    # 1. check agent_id exist or not in the dynamodb table (openadr-agents-table)
    # 2. if exist, return true
    for agent in openadr_agents_table:
        if agent['agent_id'] == agent_id:
            return True
     # 3. if not exist, return false
    return False


def send_message_to_sqs(sqs_url: str, message: str, messageGroupId: str) -> dict:
    # Create SQS client
    sqs = boto3.client('sqs')
    # Get the queue
    # queue_url =

    # Create a new message
    message_attributes = {
        'Services': {
            'DataType': 'String',
            'StringValue': 'ECS'
        },
        'Action': {
            'DataType': 'String',
            'StringValue': ECA_ACTIONS.DELETE.value
        }
    }
    MessageDeduplicationId = guid()

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=sqs_url,
        MessageBody=message,
        MessageAttributes=message_attributes,
        MessageGroupId=messageGroupId,
        MessageDeduplicationId=MessageDeduplicationId
    )
    print(f"MessageId: {response['MessageId']}")

    return response


# def guid():
#     """Return a globally unique id"""
#     return uuid.uuid4().hex[2:]

# API endpoints for CRUD operations


if __name__ == '__main__':
    # app.run(debug=True)
    # curl -i -H "Content-Type: application/json" -X POST -d '{"agent_id":"12131212"}' http://localhost:5000/creat_agent
    agent_id = "00ccff430c4bcfa1f1186f488b88fc"
    resource_id = guid()
    message_body = dict()
    # must have a agent_id
    message_body['agent_id'] = agent_id
    message_body['resource_id'] = resource_id
    message_body['market_interval_in_second'] = "300"
    # create a device and its params

    message_body['devices'] = [
        {
            "device_id": guid(),
            "device_name": "battery_0",
            "device_type": "HS",
            "device_params": {
                "battery_token": "12321321qsd",
                "battery_sn": "66354",
                "device_brand": "SONNEN_BATTERY",
            },
            "biding_price_threshold": "0.15",
            "meter_id": guid()
        }
    ]

    response = send_message_to_sqs(
        sqs_url="https://sqs.us-east-2.amazonaws.com/041414866712/openadr_workers_sqs.fifo", message=json.dumps(message_body), messageGroupId="test")
    print(f"sqs_response :{response}")
