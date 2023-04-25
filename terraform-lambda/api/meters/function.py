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
meters_table_name = os.environ["METERS_TABLE_NAME"]
meters_table_resource_id_device_id_gsi = os.environ["METERS_TABLE_RESOURCE_ID_DEVICE_ID_GSI"]
boto3.resource('dynamodb')


class MetersAttributes(Enum):
    meter_id = 'meter_id'
    device_id = 'device_id'
    resource_id = 'resource_id'
    status = 'status'
    valid_at = 'valid_at'


MetersAttributesTypes = {
    MetersAttributes.meter_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.device_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MetersAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class MetersRouteKeys(Enum):
    meters = "meters"
    meter = "meter"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == MetersRouteKeys.meters.value:
            return handle_meters_route(event=event, context=context)
        elif route_key == MetersRouteKeys.meter.value:
            return handle_meter_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Meters /db/meters
# =================================================================================================


def handle_meters_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of meters from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return post_list_of_meters_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=meters_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_meters_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=meters_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_meters_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=meters_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_meters_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of meters to dynamodb")


def put_list_of_meters_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of meters to dynamodb")


def delete_list_of_meters_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of meters from dynamodb")
    # =================================================================================================
    # Agent /db/meter/{meter_id}
    # =================================================================================================


def handle_meter_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        return handle_get_meter_from_meter_id(
            meter_id=meter_id, dynamodb_client=dynamodb_client, table_name=meters_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_meter(request_body=request_body, table_name=meters_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_meter(meter_id=meter_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        return handle_delete_meter(meter_id=meter_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/meter/{meter_id}
# ========================= #


def handle_get_meter_from_meter_id(meter_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=meter_id,
                key=MetersAttributes.meter_id.name,
                table_name=meters_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            meter_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=MetersAttributesTypes)
            return respond(err=None, res=meter_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new meter
# POST /db/meter/{meter_id}
# ========================= #

def handle_post_meter(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new meter
        meter_id = str(guid())
        item = create_item(
            primary_key_name=MetersAttributes.meter_id.name,
            primary_key_value=meter_id,
            request_body=request_body,
            attributeType=MetersAttributesTypes,
            attributes=MetersAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an meter to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an meter
# PUT /db/meter/{meter_id}
# ========================= #


def handle_put_meter(meter_id: str, request_body: dict, table_name: str = meters_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if meter_id is None:
        raise KeyError("meter_id is missing")
    try:
        # check if meter_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=meter_id,
                key=MetersAttributes.meter_id.name,
                table_name=meters_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"meter_id {meter_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=MetersAttributes.meter_id.name,
                primary_key_value=meter_id,
                request_body=request_body,
                attributeType=MetersAttributesTypes,
                attributes=MetersAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an meter to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an meter
# DELETE /db/meter/{meter_id}
# ========================= #


def handle_delete_meter(meter_id: str):
    try:
        # check if meter_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=meter_id,
                key=MetersAttributes.meter_id.name,
                table_name=meters_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=MetersAttributes.meter_id.name,
                id=meter_id,
                table_name=meters_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
