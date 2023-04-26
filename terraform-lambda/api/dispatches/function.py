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
dispatches_table_name = os.environ["DISPATCHED_TABLE_NAME"]
dispatches_table_order_id_valid_at_gsi = os.environ["DISPATCHED_TABLE_ORDER_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class DispatchesAttributes(Enum):
    order_id = 'order_id'
    record_time = 'record_time'
    quantity = 'quantity'
    valid_at = 'valid_at'


DispatchesAttributesTypes = {
    DispatchesAttributes.order_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DispatchesAttributes.record_time.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DispatchesAttributes.quantity.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    DispatchesAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class DispatchesRouteKeys(Enum):
    dispatches = "dispatches"
    dispatch = "dispatch"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == DispatchesRouteKeys.dispatches.value:
            return handle_dispatches_route(event=event, context=context)
        elif route_key == DispatchesRouteKeys.dispatch.value:
            return handle_dispatch_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Dispatches /db/dispatches
# =================================================================================================


def handle_dispatches_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of dispatches from resource id")
    elif http_method == HTTPMethods.POST.value:

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
        # update an agent
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
        return respond(err=TESSError("http method is not supported"), res=None)
