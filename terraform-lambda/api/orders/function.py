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
orders_table_name = os.environ["ORDERS_TABLE_NAME"]
orders_table_device_id_order_id_gsi = os.environ["ORDERS_TABLE_DEVICE_ID_ORDER_ID_GSI"]
orders_table_device_id_valid_at_gsi = os.environ["ORDERS_TABLE_DEVICE_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class OrdersAttributes(Enum):
    order_id = 'order_id'
    device_id = 'device_id'
    auction_id = 'auction_id'
    resource_id = 'resource_id'
    record_time = 'record_time'
    quantity = 'quantity'
    price = 'price'
    flexible = 'flexible'
    state = 'state'
    valid_at = 'valid_at'


OrdersAttributesTypes = {
    OrdersAttributes.order_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.device_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.auction_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.record_time.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    OrdersAttributes.quantity.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.flexible.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    OrdersAttributes.state.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class OrdersRouteKeys(Enum):
    orders = "orders"
    order = "order"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == OrdersRouteKeys.orders.value:
            return handle_orders_route(event=event, context=context)
        elif route_key == OrdersRouteKeys.order.value:
            return handle_order_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Orders /db/orders
# =================================================================================================


def handle_orders_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of orders from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=orders_table_name,
            hash_key_name=OrdersAttributes.order_id.name,
            attributesTypeDict=OrdersAttributesTypes
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=orders_table_name,
            hash_key_name=OrdersAttributes.order_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_order_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'order_id' not in event['pathParaorders']:
            raise KeyError("order_id is missing")
        order_id = event['pathParaorders']['order_id']
        # ========================= #
        # GET /db/agent/{agent_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=OrdersAttributes.order_id.name,
            hash_key_value=order_id,
            table_name=orders_table_name,
            attributesTypesDict=OrdersAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # POST /db/order/{order_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=OrdersAttributes.order_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=orders_table_name,
            attributeTypeDice=OrdersAttributesTypes,
            attributesEnum=OrdersAttributes,
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
        # PUT /db/order/{order_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=OrdersAttributes.order_id.name,
            hash_key_value=order_id,
            request_body=request_body,
            table_name=orders_table_name,
            attributesTypeDict=OrdersAttributesTypes,
            attributesEnum=OrdersAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        # ========================= #
        # DELETE /db/order/{order_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=OrdersAttributes.order_id.name,
            hash_key_value=order_id,
            table_name=orders_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
