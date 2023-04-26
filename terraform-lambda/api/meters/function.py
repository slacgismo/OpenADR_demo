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

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=meters_table_name,
            hash_key_name=MetersAttributes.meter_id.name,
            attributesTypeDict=MetersAttributes
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=meters_table_name,
            hash_key_name=MetersAttributes.meter_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_meter_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        # ========================= #
        # GET /db/agent/{agent_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=MetersAttributes.meter_id.name,
            hash_key_value=meter_id,
            table_name=meters_table_name,
            attributesTypesDict=MetersAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new agent
        # POST  /db/meter/{meter_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=MetersAttributes.meter_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=meters_table_name,
            attributeTypeDice=MetersAttributesTypes,
            attributesEnum=MetersAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # update an agent
        # PUT  /db/meter/{meter_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=MetersAttributes.meter_id.name,
            hash_key_value=meter_id,
            request_body=request_body,
            table_name=meters_table_name,
            attributesTypeDict=MetersAttributesTypes,
            attributesEnum=MetersAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'meter_id' not in event['pathParameters']:
            raise KeyError("meter_id is missing")
        meter_id = event['pathParameters']['meter_id']
        # ========================= #
        # delete an agent
        # DELETE  /db/meter/{meter_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=MetersAttributes.meter_id.name,
            hash_key_value=meter_id,
            table_name=meters_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
