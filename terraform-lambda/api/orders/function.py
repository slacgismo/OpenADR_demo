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

        return post_list_of_orders_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=orders_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_orders_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=orders_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_orders_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=orders_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_orders_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of orders to dynamodb")


def put_list_of_orders_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of orders to dynamodb")


def delete_list_of_orders_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of orders from dynamodb")
    # =================================================================================================
    # Agent /db/order/{order_id}
    # =================================================================================================


def handle_order_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'order_id' not in event['pathParaorders']:
            raise KeyError("order_id is missing")
        order_id = event['pathParaorders']['order_id']
        return handle_get_order_from_order_id(
            order_id=order_id, dynamodb_client=dynamodb_client, table_name=orders_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_order(request_body=request_body, table_name=orders_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_order(order_id=order_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        return handle_delete_order(order_id=order_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/order/{order_id}
# ========================= #


def handle_get_order_from_order_id(order_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=OrdersAttributes.order_id.name,
                table_name=orders_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            order_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=OrdersAttributesTypes)
            return respond(err=None, res=order_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new order
# POST /db/order/{order_id}
# ========================= #

def handle_post_order(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new order
        order_id = str(guid())
        item = create_item(
            primary_key_name=OrdersAttributes.order_id.name,
            primary_key_value=order_id,
            request_body=request_body,
            attributeType=OrdersAttributesTypes,
            attributes=OrdersAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an order to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an order
# PUT /db/order/{order_id}
# ========================= #


def handle_put_order(order_id: str, request_body: dict, table_name: str = orders_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if order_id is None:
        raise KeyError("order_id is missing")
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=OrdersAttributes.order_id.name,
                table_name=orders_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"order_id {order_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=OrdersAttributes.order_id.name,
                primary_key_value=order_id,
                request_body=request_body,
                attributeType=OrdersAttributesTypes,
                attributes=OrdersAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an order to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an order
# DELETE /db/order/{order_id}
# ========================= #


def handle_delete_order(order_id: str):
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=OrdersAttributes.order_id.name,
                table_name=orders_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=OrdersAttributes.order_id.name,
                id=order_id,
                table_name=orders_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
