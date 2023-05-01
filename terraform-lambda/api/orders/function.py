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
orders_table_name = os.environ.get("ORDERS_TABLE_NAME", None)
orders_table_device_id_order_id_gsi = os.environ.get(
    "ORDERS_TABLE_DEVICE_ID_ORDER_ID_GSI", None)
orders_table_device_id_valid_at_gsi = os.environ.get(
    "ORDERS_TABLE_DEVICE_ID_VALID_AT_GSI", None)

environment_variables_list = []
environment_variables_list.append(orders_table_name)
environment_variables_list.append(orders_table_device_id_order_id_gsi)
environment_variables_list.append(orders_table_device_id_valid_at_gsi)


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
    OrdersAttributes.order_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.device_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.resource_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.auction_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    OrdersAttributes.record_time.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    OrdersAttributes.quantity.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.price.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.flexible.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    OrdersAttributes.state.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    OrdersAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class OrdersRouteKeys(Enum):
    orders = "orders"
    order = "order"
    orders_query = "orders/query"
    orders_scan = "orders/scan"


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

        if match_path(path=path, route_key=OrdersRouteKeys.orders.value):
            return handle_orders_route(event=event, context=context)
        elif match_path(path=path, route_key=OrdersRouteKeys.order.value):
            return handle_order_route(event=event, context=context)
        elif match_path(path=path, route_key=OrdersRouteKeys.orders_query.value):
            return handle_orders_query_route(event=event, context=context)
        elif match_path(path=path, route_key=OrdersRouteKeys.orders_scan.value):
            return handle_orders_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

# =================================================================================================
# Orders /db/orders
# =================================================================================================


def handle_orders_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

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
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        # ========================= #
        # GET /db/order/{order_id}
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
        return respond(err=TESSError("http method is not supported"))


# ========================= #
# query an order
# GET /db/order/query
# ========================= #


def handle_orders_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=orders_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=OrdersAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an order
# GET /db/order/scans
# ========================= #


def handle_orders_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=orders_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=OrdersAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
