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
            'StringValue': ECA_ACTIONS.CREATE.value
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


@app.route('/agents', methods=['GET'])
def get_all_agents():

    return jsonify(agents)


@app.route('/agents/<int:id>', methods=['GET'])
def get_agent_by_id(id):
    for book in agents:
        if book['id'] == id:
            return jsonify(book)
    return jsonify({"error": "Agent not found"}), 404


@app.route('/creat_agent', methods=['POST'])
async def create_agent():
    # 1. get data from request
    data = request.get_json()
    # 2. check agent_id exist or not in the db(dynamodb or rds) table (openadr-agents-table)
    if "agent_id" not in data:
        return jsonify("agent_id not in data"), 400
    agent_id = data['agent_id']

    # 3. if exist, return agent_id exist and return status code 400
    is_exist_in_db = await check_agent_id_exist(agent_id, table_name=DYNAMODB_TABLE_NAME)
    if is_exist_in_db:
        return jsonify("agent_id exist, duplicate id"), 400

    # 4. if not exist, start to generate the information for ECS service

    # 4.1 generate vtn id, ven ids, terraform s3 key , terraform state lock with agent_id
    # check if device_ids in the dat
    ecs_service_params = dict()
    if "device_ids" not in data:
        # generate empty ECS services
        print("device_ids not in data, generate empty ECS services")
        ecs_service_params = generate_empty_ecs_services_params(agent_id)

    else:
        device_ids = data['device_ids']
        if len(device_ids) == 0:
            print("device_ids not in data, generate empty ECS services")
        # start to generate ECS services
        ecs_service_params = generate_ecs_services_param_with_devices(
            agent_id=agent_id, device_ids=device_ids)
    # send the params to SQS queue
    sqs_response = send_message_to_sqs(
        sqs_url=SQS_URL, message=json.dumps(ecs_service_params))
    print(f"sqs_response :{sqs_response}")
    # 7. async wait for the worker to finish the task
    return jsonify("create a new agent"), 201


@ app.route('/agents/<int:id>', methods=['PUT'])
def update_agent(id):
    data = request.json
    # 1. get data from request
    # 2. check agent_id exist or not in the dynamodb table (openadr-agents-table)
    # 3. if not exist, return agent_id not exist and return status code 400
    # 4. if exist, update the agent_id, vtn_id, ven_ids, task definition file location
    # 5. send a message to SQS queue to invoke the worker
    # 6. async wait for the worker to finish the task
    return jsonify({"error": "Book not found"}), 404


@ app.route('/agents/<int:id>', methods=['DELETE'])
def delete_agent(id):
    # 1. get data from request
    # 2. check agent_id exist or not in the dynamodb table (openadr-agents-table)
    # 3. if not exist, return agent_id not exist and return status code 400
    # 4. send a message to SQS queue to invoke the worker
    # 5. async wait for the worker to finish the task
    # 6. if task completed, delete the agent_id, vtn_id, ven_ids, task definition file location
    return jsonify({"error": "Book not found"}), 404


if __name__ == '__main__':
    # app.run(debug=True)
    # curl -i -H "Content-Type: application/json" -X POST -d '{"agent_id":"12131212"}' http://localhost:5000/creat_agent
    agent_id = guid()
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
