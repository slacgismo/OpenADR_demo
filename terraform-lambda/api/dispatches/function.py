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

        return post_list_of_dispatches_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=dispatches_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_dispatches_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=dispatches_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_dispatches_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=dispatches_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_dispatches_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of dispatches to dynamodb")


def put_list_of_dispatches_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of dispatches to dynamodb")


def delete_list_of_dispatches_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of dispatches from dynamodb")
    # =================================================================================================
    # Agent /db/dispatch/{order_id}
    # =================================================================================================


def handle_dispatch_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        return handle_get_dispatch_from_order_id(
            order_id=order_id, dynamodb_client=dynamodb_client, table_name=dispatches_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_dispatch(request_body=request_body, table_name=dispatches_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_dispatch(order_id=order_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        return handle_delete_dispatch(order_id=order_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/dispatch/{order_id}
# ========================= #


def handle_get_dispatch_from_order_id(order_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=DispatchesAttributes.order_id.name,
                table_name=dispatches_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            dispatch_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=DispatchesAttributesTypes)
            return respond(err=None, res=dispatch_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new dispatch
# POST /db/dispatch/{order_id}
# ========================= #

def handle_post_dispatch(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new dispatch
        order_id = str(guid())
        item = create_item(
            primary_key_name=DispatchesAttributes.order_id.name,
            primary_key_value=order_id,
            request_body=request_body,
            attributeType=DispatchesAttributesTypes,
            attributes=DispatchesAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an dispatch to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an dispatch
# PUT /db/dispatch/{order_id}
# ========================= #


def handle_put_dispatch(order_id: str, request_body: dict, table_name: str = dispatches_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if order_id is None:
        raise KeyError("order_id is missing")
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=DispatchesAttributes.order_id.name,
                table_name=dispatches_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"order_id {order_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=DispatchesAttributes.order_id.name,
                primary_key_value=order_id,
                request_body=request_body,
                attributeType=DispatchesAttributesTypes,
                attributes=DispatchesAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an dispatch to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an dispatch
# DELETE /db/dispatch/{order_id}
# ========================= #


def handle_delete_dispatch(order_id: str):
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=DispatchesAttributes.order_id.name,
                table_name=dispatches_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=DispatchesAttributes.order_id.name,
                id=order_id,
                table_name=dispatches_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
