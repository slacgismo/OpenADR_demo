import json
import asyncio
import boto3
import json
import time
import os
from enum import Enum
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import uuid
import re
# cmmmon_utils, constants is from shared layer
from common_utils import respond, TESSError, put_item_to_dynamodb, get_item_from_dynamodb, delete_item_from_dynamodb, deserializer_dynamodb_data_to_json_format, get_path, HTTPMethods, guid, create_item

dynamodb_client = boto3.client('dynamodb')
agents_table_name = os.environ["AGENTS_TABLE_NAME"]
agents_table_resource_id_valid_at_gsi = os.environ["AGENTS_TABLE_RESOURCE_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class AgentsAttributes(Enum):
    agent_id = 'agent_id'
    resource_id = 'resource_id'
    status = 'status'
    valid_at = 'valid_at'


AgentsAttributesTypes = {
    AgentsAttributes.agent_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AgentsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class AgentsRouteKeys(Enum):
    agents = "agents"
    agent = "agent"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == AgentsRouteKeys.agents.value:
            return handle_agents_route(event=event, context=context)
        elif route_key == AgentsRouteKeys.agent.value:
            return handle_agent_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Agents /db/agents
# =================================================================================================


def handle_agents_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of agents from resource id")
        # get_list_of_agents_from_reource_id_with_pagination(
        #     resource_id=resource_id,
        #     dynamodb_client=dynamodb_client,
        #     table_name=agents_table_name,
        #     table_GSI=agents_table_resource_id_valid_at_gsi,
        #     request_body=request_body
        # )
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return post_list_of_agents_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=agents_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_agents_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=agents_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_agents_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=agents_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_agents_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of agents to dynamodb")


def put_list_of_agents_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of agents to dynamodb")


def delete_list_of_agents_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of agents from dynamodb")
    # =================================================================================================
    # Agent /db/agent/{agent_id}
    # =================================================================================================


def handle_agent_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        return handle_get_agent_from_agent_id(
            agent_id=agent_id, dynamodb_client=dynamodb_client, table_name=agents_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_agent(request_body=request_body, table_name=agents_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_agent(agent_id=agent_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        return handle_delete_agent(agent_id=agent_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/agent/{agent_id}
# ========================= #


def handle_get_agent_from_agent_id(agent_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=agent_id,
                key=AgentsAttributes.agent_id.name,
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
                item=item, attributesTypes=AgentsAttributesTypes)
            return respond(err=None, res=agent_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new agent
# POST /db/agent/{agent_id}
# ========================= #

def handle_post_agent(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new agent
        agent_id = str(guid())
        item = create_item(
            primary_key_name=AgentsAttributes.agent_id.name,
            primary_key_value=agent_id,
            request_body=request_body,
            attributeType=AgentsAttributesTypes,
            attributes=AgentsAttributes
        )
        # item = create_item(
        #     agent_id=agent_id,
        #     resource_id=resource_id,
        #     status=status,
        #     valid_at=valid_at
        # )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an agent to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an agent
# PUT /db/agent/{agent_id}
# ========================= #


def handle_put_agent(agent_id: str, request_body: dict, table_name: str = agents_table_name, dynamodb_client: boto3.client = dynamodb_client):
    resource_id = request_body.get('resource_id', None)
    status = request_body.get('status', None)
    if resource_id is None or status is None:
        return respond(err=TESSError("resource_id or status is missing"), res=None)

    try:
        # check if agent_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=agent_id,
                key=AgentsAttributes.agent_id.name,
                table_name=agents_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"agent_id {agent_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=AgentsAttributes.agent_id.name,
                primary_key_value=agent_id,
                request_body=request_body,
                attributeType=AgentsAttributesTypes,
                attributes=AgentsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an agent to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an agent
# DELETE /db/agent/{agent_id}
# ========================= #


def handle_delete_agent(agent_id: str):
    try:
        # check if agent_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=agent_id,
                key=AgentsAttributes.agent_id.name,
                table_name=agents_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=AgentsAttributes.agent_id.name,
                id=agent_id,
                table_name=agents_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
