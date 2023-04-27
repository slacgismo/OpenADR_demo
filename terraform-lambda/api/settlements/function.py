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
settlements_table_name = os.environ.get("SETTLEMENTS_TABLE_NAME", None)

environment_variables_list = []
environment_variables_list.append(settlements_table_name)


class SettlementsAttributes(Enum):
    order_id = 'order_id'
    record_time = 'record_time'
    cost = 'cost'
    valid_at = 'valid_at'


SettlementsAttributesTypes = {
    SettlementsAttributes.order_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettlementsAttributes.record_time.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    SettlementsAttributes.cost.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    SettlementsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class SettlementsRouteKeys(Enum):
    settlements = "settlements"
    settlement = "settlement"
    settlements_query = "settlements/query"
    settlements_scan = "settlements/scan"


def handler(event, context):
    try:
        # check the environment variables
        if None in environment_variables_list:
            raise Exception(
                f"environment variables are not set :{environment_variables_list}")

        # parse the path
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        if match_path(path=path, route_key=SettlementsRouteKeys.settlements.value):
            return handle_settlements_route(event=event, context=context)
        elif match_path(path=path, route_key=SettlementsRouteKeys.settlement.value):
            return handle_settlement_route(event=event, context=context)
        elif match_path(path=path, route_key=SettlementsRouteKeys.settlements_query.value):
            return handle_settlements_query_route(event=event, context=context)
        elif match_path(path=path, route_key=SettlementsRouteKeys.settlements_scan.value):
            return handle_settlements_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Settlements /db/settlements
# =================================================================================================


def handle_settlements_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of settlements from settlement id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=settlements_table_name,
            hash_key_name=SettlementsAttributes.order_id.name,
            attributesTypeDict=SettlementsAttributesTypes,
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=settlements_table_name,
            hash_key_name=SettlementsAttributes.order_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_settlement_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        # ========================= #
        # GET /db/settlement/{order_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=SettlementsAttributes.order_id.name,
            hash_key_value=order_id,
            table_name=settlements_table_name,
            attributesTypesDict=SettlementsAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new settlement
        # POST /db/settlement/{order_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=SettlementsAttributes.order_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=settlements_table_name,
            attributeTypeDice=SettlementsAttributesTypes,
            attributesEnum=SettlementsAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # update an settlement
        # PUT /db/settlement/{order_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=SettlementsAttributes.order_id.name,
            hash_key_value=order_id,
            request_body=request_body,
            table_name=settlements_table_name,
            attributesTypeDict=SettlementsAttributesTypes,
            attributesEnum=SettlementsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        # ========================= #
        # delete an settlement
        # DELETE /db/settlement/{order_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=SettlementsAttributes.order_id.name, hash_key_value=order_id, table_name=settlements_table_name, dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
# ========================= #
# query an settlement
# GET /db/settlement/query
# ========================= #


def handle_settlements_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=settlements_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=SettlementsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an settlement
# GET /db/settlement/scans
# ========================= #


def handle_settlements_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=settlements_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=SettlementsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")