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
settlements_table_name = os.environ["SETTLEMENTS_TABLE_NAME"]

boto3.resource('dynamodb')


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


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == SettlementsRouteKeys.settlements.value:
            return handle_settlements_route(event=event, context=context)
        elif route_key == SettlementsRouteKeys.settlement.value:
            return handle_settlement_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

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

        return post_list_of_settlements_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settlements_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_settlements_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settlements_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_settlements_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settlements_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_settlements_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of settlements to dynamodb")


def put_list_of_settlements_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of settlements to dynamodb")


def delete_list_of_settlements_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of settlements from dynamodb")
    # =================================================================================================
    # Agent /db/settlement/{order_id}
    # =================================================================================================


def handle_settlement_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        return handle_get_settlement_from_order_id(
            order_id=order_id, dynamodb_client=dynamodb_client, table_name=settlements_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_settlement(request_body=request_body, table_name=settlements_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_settlement(order_id=order_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'order_id' not in event['pathParameters']:
            raise KeyError("order_id is missing")
        order_id = event['pathParameters']['order_id']
        return handle_delete_settlement(order_id=order_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/settlement/{order_id}
# ========================= #


def handle_get_settlement_from_order_id(order_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=SettlementsAttributes.order_id.name,
                table_name=settlements_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            settlement_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=SettlementsAttributesTypes)
            return respond(err=None, res=settlement_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new settlement
# POST /db/settlement/{order_id}
# ========================= #

def handle_post_settlement(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new settlement
        order_id = str(guid())
        item = create_item(
            primary_key_name=SettlementsAttributes.order_id.name,
            primary_key_value=order_id,
            request_body=request_body,
            attributeType=SettlementsAttributesTypes,
            attributes=SettlementsAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an settlement to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an settlement
# PUT /db/settlement/{order_id}
# ========================= #


def handle_put_settlement(order_id: str, request_body: dict, table_name: str = settlements_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if order_id is None:
        raise KeyError("order_id is missing")
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=SettlementsAttributes.order_id.name,
                table_name=settlements_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"order_id {order_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=SettlementsAttributes.order_id.name,
                primary_key_value=order_id,
                request_body=request_body,
                attributeType=SettlementsAttributesTypes,
                attributes=SettlementsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an settlement to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an settlement
# DELETE /db/settlement/{order_id}
# ========================= #


def handle_delete_settlement(order_id: str):
    try:
        # check if order_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=order_id,
                key=SettlementsAttributes.order_id.name,
                table_name=settlements_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=SettlementsAttributes.order_id.name,
                id=order_id,
                table_name=settlements_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
