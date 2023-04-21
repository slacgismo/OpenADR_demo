import json
import asyncio
import boto3
import json
import time
import os
from enum import Enum
dynamodb_client = boto3.client('dynamodb')
agents_table_name = os.environ["AGENTS_TABLE_NAME"]


class AgentsTableAttributes(Enum):
    AGENT_ID = 'agent_id'
    RESOURCE_ID = 'resource_id'
    STATUS = 'status'
    VALID_AT = 'valid_at'


"""
list of agents
Get /db/agents?resource_id=<resource_id>&valid_at=<valid_at>, Get a list of agents id
"""


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            """
            get one agent
            Get /db/agent/{agent_id}, Get an agent info. If there is already a record for <agent_id>,
            then it returns the previous data entry. Otherwise, return the new data entry.
            """
            # check if agent_id is in path
            if 'agent_id' in event['pathParameters']:
                agent_id = event['pathParameters']['agent_id']
                # return asyncio.run(get_item_from_dynamodb(id=agent_id, key=AgentsTableAttributes.AGENT_ID.value, table_name=agents_table_name, dynamodb_client=dynamodb_client))
                return asyncio.run(
                    get_agent_item_from_dynamodb(
                        agent_id=agent_id, table_name=agents_table_name, dynamodb_client=dynamodb_client
                    )
                )
            else:
                error_message = {
                    'error': 'agent_id is not in body'
                }
                return create_json_message(
                    statusCode=404,
                    body_payload=error_message
                )
                # return {
                #     'statusCode': 404,
                #     'headers': {'Content-Type': 'application/json'},
                #     'body': json.dumps({'message': "agent_id is not in path"})
                # }

        elif http_method == 'PUT':

            """
            PUT /db/agent/{agent_id}
            Put an agent record to table
            """
            if 'agent_id' in event['pathParameters']:
                agent_id = event['pathParameters']['agent_id']
                request_body = json.loads(event['body'])
                resource_id = request_body.get('resource_id', None)
                status = request_body.get('status', None)
                if resource_id is None or status is None:
                    error_message = {
                        'error': 'resource_id or status not in body'
                    }
                    return create_json_message(
                        statusCode=404,
                        body_payload=error_message
                    )
                    # return {
                    #     'statusCode': 404,
                    #     'headers': {'Content-Type': 'application/json'},
                    #     'body': json.dumps({'message': "resource_id or status is not in body"})
                    # }

                valid_at = int(time.time())

                # save data to dynamodb
                return asyncio.run(put_agent_info_to_dynamodb(
                    agent_id=agent_id,
                    resource_id=resource_id,
                    status=status,
                    valid_at=valid_at,
                    table_name=agents_table_name,
                    dynamodb_client=dynamodb_client,
                ))

        elif http_method == "DELETE":
            """
            Delete /db/agent/{agent_id}
            Delete an agent record to table
            """
            if 'agent_id' in event['pathParameters']:
                agent_id = event['pathParameters']['agent_id']
                return asyncio.run(delete_item_from_dynamodb(id=agent_id, key=AgentsTableAttributes.AGENT_ID.value, table_name=agents_table_name, dynamodb_client=dynamodb_client))
            else:
                error_message = {
                    'error': 'agent_id is not in path'
                }
                return create_json_message(
                    statusCode=404,
                    body_payload=error_message
                )
        # return {
        #     'statusCode': 404,
        #     'headers': {'Content-Type': 'application/json'},
        #     'body': json.dumps({'message': "agent_id is not in path"})
        # }
    except Exception as e:
        error_message = {
            'error': str(e)
        }
        return create_json_message(
            statusCode=500,
            body_payload=error_message
        )


async def put_agent_info_to_dynamodb(agent_id: str,
                                     resource_id: str,
                                     status: str,
                                     valid_at: int,
                                     table_name: str,
                                     dynamodb_client):
    try:
        response = await asyncio.to_thread(dynamodb_client.put_item,
                                           TableName=table_name,
                                           Item={
                                               'agent_id': {'S': agent_id},
                                               'resource_id': {'S': resource_id},
                                               'status': {'N': status},
                                               'valid_at': {'N': str(valid_at)}
                                           }
                                           )
        return create_json_message(
            statusCode=200,
            body_payload=response
        )
    except Exception as e:
        error_message = {
            'error': str(e)
        }
        return create_json_message(
            statusCode=500,
            body_payload=error_message
        )


async def get_agent_item_from_dynamodb(
        agent_id: str,
        table_name: str,
        dynamodb_client,
) -> dict:
    try:
        response = await asyncio.to_thread(get_item_from_dynamodb(id=agent_id, key=AgentsTableAttributes.AGENT_ID.value, table_name=table_name, dynamodb_client=dynamodb_client))
        # if faild to get item from dynamodb
        # return {
        #     'statusCode': 200,
        #     'headers': {'Content-Type': 'application/json'},
        #     'body': json.dumps(response)
        # }
        return create_json_message(
            statusCode=200,
            body_payload=response
        )
    except Exception as e:
        error_message = {
            'error': str(e)
        }
        return create_json_message(
            statusCode=500,
            body_payload=error_message
        )
        # return {
        #     'statusCode': 500,
        #     'headers': {'Content-Type': 'application/json'},
        #     'body': json.dumps(error_message)
        # }


# shared layer function

async def get_item_from_dynamodb(id: str, key: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(
            dynamodb_client.get_item,
            TableName=table_name,
            Key={
                key: {'S': id}
            }
        )
        return response
    except Exception as e:
        raise Exception(e)


def create_json_message(
    body_payload: dict,
    statusCode: int,
    headers: dict =
    {'Content-Type': 'application/json'}
):
    return {
        'statusCode': statusCode,
        'headers': headers,
        'body': json.dumps(body_payload)
    }


async def delete_item_from_dynamodb(key: str, id: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(dynamodb_client.delete_item,
                                           TableName=table_name,
                                           Key={
                                               key: {'S': id}
                                           }
                                           )
        return create_json_message(
            statusCode=200,
            body_payload=response
        )
    except Exception as e:
        error_message = {
            'error': str(e)
        }
        return create_json_message(
            statusCode=500,
            body_payload=error_message
        )
