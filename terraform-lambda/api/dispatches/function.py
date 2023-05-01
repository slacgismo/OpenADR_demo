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
# dispatches_table_name = os.environ["DISPATCHED_TABLE_NAME"]
# dispatches_table_order_id_valid_at_gsi = os.environ["DISPATCHED_TABLE_ORDER_ID_VALID_AT_GSI"]
dispatches_table_name = os.environ.get("DISPATCHED_TABLE_NAME", None)
dispatches_table_order_id_valid_at_gsi = os.environ.get(
    "DISPATCHED_TABLE_ORDER_ID_VALID_AT_GSI", None)
boto3.resource('dynamodb')


environment_variables_list = []
environment_variables_list.append(dispatches_table_name)
environment_variables_list.append(dispatches_table_order_id_valid_at_gsi)


class DispatchesAttributes(Enum):
    order_id = 'order_id'
    record_time = 'record_time'
    quantity = 'quantity'
    valid_at = 'valid_at'


DispatchesAttributesTypes = {
    DispatchesAttributes.order_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DispatchesAttributes.record_time.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DispatchesAttributes.quantity.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    DispatchesAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class DispatchesRouteKeys(Enum):
    dispatches = "dispatches"
    dispatch = "dispatch"
    dispatches_query = "dispatches/query"
    dispatches_scan = "dispatches/scan"


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

        if match_path(path=path, route_key=DispatchesRouteKeys.dispatches.value):
            return handle_dispatches_route(event=event, context=context)
        elif match_path(path=path, route_key=DispatchesRouteKeys.dispatch.value):
            return handle_dispatch_route(event=event, context=context)
        elif match_path(path=path, route_key=DispatchesRouteKeys.dispatches_query.value):
            return handle_dispatches_query_route(event=event, context=context)
        elif match_path(path=path, route_key=DispatchesRouteKeys.dispatches_scan.value):
            return handle_dispatches_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

# =================================================================================================
# Dispatches /db/dispatches
# =================================================================================================


def handle_dispatches_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=dispatches_table_name,
            hash_key_name=DispatchesAttributes.order_id.name,
            attributesTypeDict=DispatchesAttributesTypes,
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=dispatches_table_name,
            hash_key_name=DispatchesAttributes.order_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_dispatch_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # ========================= #
        # GET /db/dispatch/{order_id}
        # ========================= #
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']

        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=DispatchesAttributes.order_id.name,
            hash_key_value=order_id,
            table_name=dispatches_table_name,
            attributesTypesDict=DispatchesAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        # ========================= #
        # POST /db/dispatch/{order_id}
        # ========================= #
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_create_item_to_dynamodb(
            hash_key_name=DispatchesAttributes.order_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=dispatches_table_name,
            attributeTypeDice=DispatchesAttributesTypes,
            attributesEnum=DispatchesAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:

        # ========================= #
        # update an dispatch
        # PUT /db/dispatch/{order_id}
        # ========================= #

        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=DispatchesAttributes.order_id.name,
            hash_key_value=order_id,
            request_body=request_body,
            table_name=dispatches_table_name,
            attributesTypeDict=DispatchesAttributesTypes,
            attributesEnum=DispatchesAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        # ========================= #
        # DELETE /db/dispatch/{order_id}
        # ========================= #
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']

        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=DispatchesAttributes.order_id.name,
            hash_key_value=order_id,
            table_name=dispatches_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))


# ========================= #
# query an dispatch
# GET /db/dispatch/query
# ========================= #


def handle_dispatches_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=dispatches_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=DispatchesAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an dispatch
# GET /db/dispatch/scans
# ========================= #


def handle_dispatches_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=dispatches_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=DispatchesAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
