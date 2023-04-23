import json
import asyncio
import boto3
import json
import time
import os
from enum import Enum
from decimal import Decimal
# cmmmon_utils is from shared layer
from common_utils import respond, TESSError, decimal_default, put_item_to_dynamodb, get_item_from_dynamodb, delete_item_from_dynamodb, deserializer_dynamodb_data_to_json_format


dynamodb_client = boto3.client('dynamodb')
agents_table_name = os.environ["AGENTS_TABLE_NAME"]
boto3.resource('dynamodb')


class AgentsAttributesReturnType(Enum):
    agent_id = 'string'
    resource_id = 'string'
    status = 'integer'
    valid_at = 'integer'


class AgentsTableAttributes(Enum):
    agent_id = 'S'
    resource_id = 'S'
    status = 'N'
    valid_at = 'N'


# TODO: add get lists of agents
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
                response = asyncio.run(
                    get_item_from_dynamodb(
                        id=agent_id,
                        key=AgentsTableAttributes.agent_id.name,
                        table_name=agents_table_name,
                        dynamodb_client=dynamodb_client
                    )
                )
                item = response.get('Item', None)
                if item is None:
                    return respond(err=TESSError("no object is found"), res=None)
                else:
                    # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
                    agent_data = deserializer_dynamodb_data_to_json_format(
                        item=item, return_attributes=AgentsAttributesReturnType)

                    return respond(err=None, res=agent_data)

            else:
                return respond(err=TESSError("agent_id is missing"), res=None)

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
                    return respond(err=TESSError("resource_id or status is missing"), res=None)

                valid_at = int(time.time())
                # create item
                item = {
                    AgentsTableAttributes.agent_id.name: {AgentsTableAttributes.agent_id.value: agent_id},
                    AgentsTableAttributes.resource_id.name: {AgentsTableAttributes.resource_id.value: resource_id},
                    AgentsTableAttributes.status.name: {AgentsTableAttributes.status.value: str(status)},
                    AgentsTableAttributes.valid_at.name: {
                        AgentsTableAttributes.valid_at.value: str(valid_at)}
                }
                # save data to dynamodb
                response = asyncio.run(put_item_to_dynamodb(
                    item=item,
                    table_name=agents_table_name,
                    dynamodb_client=dynamodb_client,
                ))
                return respond(err=None, res="pud data to dynamodb success")
        elif http_method == "DELETE":
            """
            Delete /db/agent/{agent_id}
            Delete an agent record to table
            """
            if 'agent_id' in event['pathParameters']:
                agent_id = event['pathParameters']['agent_id']
                # chec if agent_id exist
                response = asyncio.run(
                    get_item_from_dynamodb(
                        id=agent_id,
                        key=AgentsTableAttributes.agent_id.name,
                        table_name=agents_table_name,
                        dynamodb_client=dynamodb_client
                    )
                )
                item = response.get('Item', None)
                if item is None:
                    return respond(err=TESSError(f"agent_id {agent_id} does not exist"), res=None)

                return asyncio.run(delete_item_from_dynamodb(id=agent_id, key=AgentsTableAttributes.agent_id.name, table_name=agents_table_name, dynamodb_client=dynamodb_client))
            else:
                return respond(err=TESSError("agent_id is missing"), res=None)

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)
