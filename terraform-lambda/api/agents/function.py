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
from common_utils import respond, TESSError, get_path, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb
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

    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=agents_table_name,
            hash_key_name=AgentsAttributes.agent_id.name,
            attributesTypeDict=AgentsAttributesTypes
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=agents_table_name,
            hash_key_name=AgentsAttributes.agent_id.name,
        )
    else:
        raise Exception("http method is not supported")

    # =================================================================================================
    # Agent /db/agent/{agent_id}
    # =================================================================================================


def handle_agent_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        # ========================= #
        # GET /db/agent/{agent_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=AgentsAttributes.agent_id.name,
            hash_key_value=agent_id,
            table_name=agents_table_name,
            attributesTypesDict=AgentsAttributesTypes,
            dynamodb_client=dynamodb_client
        )

    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new agent
        # POST /db/agent/{agent_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=AgentsAttributes.agent_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=agents_table_name,
            attributeTypeDice=AgentsAttributesTypes,
            attributesEnum=AgentsAttributes,
            dynamodb_client=dynamodb_client

        )

    elif http_method == HTTPMethods.PUT.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # update an agent
        # PUT /db/agent/{agent_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=AgentsAttributes.agent_id.name,
            hash_key_value=agent_id,
            request_body=request_body,
            table_name=agents_table_name,
            attributesTypeDict=AgentsAttributesTypes,
            attributesEnum=AgentsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        # ========================= #
        # delete an agent
        # DELETE /db/agent/{agent_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=AgentsAttributes.agent_id.name, hash_key_value=agent_id, table_name=agents_table_name, dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
