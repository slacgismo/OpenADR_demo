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
readings_table_name = os.environ["READINGS_TABLE_NAME"]
readings_table_meter_id_gsi = os.environ["READINGS_TABLE_METER_ID_GSI"]
readings_table_meter_id_valid_at_gsi = os.environ["READINGS_TABLE_METER_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class ReadingsAttributes(Enum):
    reading_id = 'reading_id'
    meter_id = 'meter_id'
    name = 'name'
    value = 'value'
    valid_at = 'valid_at'


ReadingsAttributesTypes = {
    ReadingsAttributes.reading_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ReadingsAttributes.meter_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ReadingsAttributes.name.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ReadingsAttributes.value.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ReadingsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class ReadingsRouteKeys(Enum):
    readings = "readings"
    reading = "reading"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == ReadingsRouteKeys.readings.value:
            return handle_readings_route(event=event, context=context)
        elif route_key == ReadingsRouteKeys.reading.value:
            return handle_reading_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Readings /db/readings
# =================================================================================================


def handle_readings_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of readings from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=readings_table_name,
            hash_key_name=ReadingsAttributes.reading_id.name,
            attributesTypeDict=ReadingsAttributesTypes
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=readings_table_name,
            hash_key_name=ReadingsAttributes.reading_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_reading_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        # ========================= #
        # GET /db/agent/{agent_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=ReadingsAttributes.reading_id.name,
            hash_key_value=reading_id,
            table_name=readings_table_name,
            attributesTypesDict=ReadingsAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # POST /db/reading/{reading_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=ReadingsAttributes.reading_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=readings_table_name,
            attributeTypeDice=ReadingsAttributesTypes,
            attributesEnum=ReadingsAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # PUT /db/reading/{reading_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=ReadingsAttributes.reading_id.name,
            hash_key_value=reading_id,
            request_body=request_body,
            table_name=readings_table_name,
            attributesTypeDict=ReadingsAttributesTypes,
            attributesEnum=ReadingsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        # ========================= #
        # DELETE /db/reading/{reading_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=ReadingsAttributes.reading_id.name,
            hash_key_value=reading_id,
            table_name=readings_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
