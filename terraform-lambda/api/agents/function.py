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
from common_utils import respond, TESSError, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb, handle_query_items_from_dynamodb, handle_scan_items_from_dynamodb, match_path

dynamodb_client = boto3.client('dynamodb')
agents_table_name = os.environ.get("AGENTS_TABLE_NAME", None)
agents_table_resource_id_valid_at_gsi = os.environ.get(
    "AGENTS_TABLE_RESOURCE_ID_VALID_AT_GSI", None)


environment_variables_list = []
environment_variables_list.append(agents_table_name)
environment_variables_list.append(agents_table_resource_id_valid_at_gsi)

# =================================================================================================
# Constants
# =================================================================================================


class AgentsAttributes(Enum):
    agent_id = 'agent_id'
    resource_id = 'resource_id'
    agent_status = 'agent_status'
    valid_at = 'valid_at'


AgentsAttributesTypes = {
    AgentsAttributes.agent_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.resource_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.agent_status.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AgentsAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class AgentsRouteKeys(Enum):
    agents = "agents"
    agent = "agent"
    agents_query = "agents/query"
    agents_scan = "agents/scan"

# =================================================================================================
# Main handler
# =================================================================================================


def handler(event, context):
    try:
        # check the environment variables
        if None in environment_variables_list:
            raise Exception(
                f"environment variables are not set :{environment_variables_list}")

        # parse the path
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"))

        if match_path(path=path, route_key=AgentsRouteKeys.agents.value):
            return handle_agents_route(event=event, context=context)
        elif match_path(path=path, route_key=AgentsRouteKeys.agent.value):
            return handle_agent_route(event=event, context=context)
        elif match_path(path=path, route_key=AgentsRouteKeys.agents_query.value):
            return handle_agents_query_route(event=event, context=context)
        elif match_path(path=path, route_key=AgentsRouteKeys.agents_scan.value):
            return handle_agents_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

    # =================================================================================================
    # Agents /db/agents/{get_items_action}
    # =================================================================================================


def handle_agents_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

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
        return respond(err=TESSError("http method is not supported"))

# ========================= #
# query an agent
# GET /db/agent/query
# ========================= #


def handle_agents_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=agents_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=AgentsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an agent
# GET /db/agent/scans
# ========================= #


def handle_agents_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=agents_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=AgentsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
