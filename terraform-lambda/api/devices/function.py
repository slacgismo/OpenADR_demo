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
devices_table_name = os.environ["DEVICES_TABLE_NAME"]
devices_table_agent_id_valid_at_gsi = os.environ["DEVICES_TABLE_AGENT_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class DevicesAttributes(Enum):
    device_id = 'device_id'
    agent_id = 'agent_id'
    device_type = 'device_type'
    device_model = 'device_model'
    flexible = 'flexible'
    status = 'status'
    valid_at = 'valid_at'


DevicesAttributesTypes = {
    DevicesAttributes.device_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.agent_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.device_type.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.device_model.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.flexible.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DevicesAttributes.status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DevicesAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class DevicesRouteKeys(Enum):
    devices = "devices"
    device = "device"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == DevicesRouteKeys.devices.value:
            return handle_devices_route(event=event, context=context)
        elif route_key == DevicesRouteKeys.device.value:
            return handle_device_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Devices /db/devices
# =================================================================================================


def handle_devices_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of devices from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return post_list_of_devices_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=devices_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_devices_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=devices_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_devices_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=devices_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_devices_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of devices to dynamodb")


def put_list_of_devices_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of devices to dynamodb")


def delete_list_of_devices_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of devices from dynamodb")
    # =================================================================================================
    # Agent /db/device/{device_id}
    # =================================================================================================


def handle_device_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        return handle_get_device_from_device_id(
            device_id=device_id, dynamodb_client=dynamodb_client, table_name=devices_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_device(request_body=request_body, table_name=devices_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_device(device_id=device_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        return handle_delete_device(device_id=device_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/device/{device_id}
# ========================= #


def handle_get_device_from_device_id(device_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=device_id,
                key=DevicesAttributes.device_id.name,
                table_name=devices_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            device_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=DevicesAttributesTypes)
            return respond(err=None, res=device_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new device
# POST /db/device/{device_id}
# ========================= #

def handle_post_device(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new device
        device_id = str(guid())
        item = create_item(
            primary_key_name=DevicesAttributes.device_id.name,
            primary_key_value=device_id,
            request_body=request_body,
            attributeType=DevicesAttributesTypes,
            attributes=DevicesAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an device to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an device
# PUT /db/device/{device_id}
# ========================= #


def handle_put_device(device_id: str, request_body: dict, table_name: str = devices_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if device_id is None:
        raise Exception("device_id is missing")

    try:
        # check if device_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=device_id,
                key=DevicesAttributes.device_id.name,
                table_name=devices_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"device_id {device_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=DevicesAttributes.device_id.name,
                primary_key_value=device_id,
                request_body=request_body,
                attributeType=DevicesAttributesTypes,
                attributes=DevicesAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an device to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an device
# DELETE /db/device/{device_id}
# ========================= #


def handle_delete_device(device_id: str):
    try:
        # check if device_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=device_id,
                key=DevicesAttributes.device_id.name,
                table_name=devices_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=DevicesAttributes.device_id.name,
                id=device_id,
                table_name=devices_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
