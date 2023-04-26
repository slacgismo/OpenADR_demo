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
        # =================================================================================================
        # GET /db/devices
        # =================================================================================================
        if 'agent_id' not in event['pathParameters']:
            raise KeyError("agent_id is missing")
        agent_id = event['pathParameters']['agent_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of devices from resource id")
    elif http_method == HTTPMethods.POST.value:
       # =================================================================================================
        # POST /db/devices
        # =================================================================================================
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=devices_table_name,
            hash_key_name=DevicesAttributes.device_id.name,
            attributesTypeDict=DevicesAttributesTypes
        )

    elif http_method == HTTPMethods.DELETE.value:
        # =================================================================================================
        # DELETE /db/devices
        # =================================================================================================

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=devices_table_name,
            hash_key_name=DevicesAttributes.device_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_device_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        # ========================= #
        # GET /db/device/{device_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=DevicesAttributes.device_id.name,
            hash_key_value=device_id,
            table_name=devices_table_name,
            attributesTypesDict=DevicesAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new agent
        # POST /db/device/{device_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=DevicesAttributes.device_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=devices_table_name,
            attributeTypeDice=DevicesAttributesTypes,
            attributesEnum=DevicesAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.PUT.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # update an agent
        # PUT  /db/device/{device_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=DevicesAttributes.device_id.name,
            hash_key_value=device_id,
            request_body=request_body,
            table_name=devices_table_name,
            attributesTypeDict=DevicesAttributesTypes,
            attributesEnum=DevicesAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'device_id' not in event['pathParameters']:
            raise KeyError("device_id is missing")
        device_id = event['pathParameters']['device_id']
        # ========================= #
        # delete an device
        # DELETE  /db/device/{device_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=DevicesAttributes.device_id.name,
            hash_key_value=device_id,
            table_name=devices_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
