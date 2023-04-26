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
weather_table_name = os.environ["WEATHER_TABLE_NAME"]
weather_table_zip_code_valid_at_gsi = os.environ["WEATHER_TABLE_ZIP_CODE_VALID_AT_GSI"]
boto3.resource('dynamodb')


class WeathersAttributes(Enum):
    weather_id = 'weather_id'
    zip_code = 'zip_code'
    temperature = 'temperature'
    humidity = 'humidity'
    solar = 'solar'
    wind_speed = 'wind_speed'
    wind_direction = 'wind_direction'
    valid_at = 'valid_at'


WeathersAttributesTypes = {
    WeathersAttributes.weather_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    WeathersAttributes.zip_code.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    WeathersAttributes.temperature.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.humidity.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.solar.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.wind_speed.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.wind_direction.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class WeathersRouteKeys(Enum):
    weathers = "weathers"
    weather = "weather"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == WeathersRouteKeys.weathers.value:
            return handle_weathers_route(event=event, context=context)
        elif route_key == WeathersRouteKeys.weather.value:
            return handle_weather_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Weathers /db/weathers
# =================================================================================================


def handle_weathers_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of weathers from weather id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=weather_table_name,
            hash_key_name=WeathersAttributes.weather_id.name,
            attributesTypeDict=WeathersAttributesTypes,
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=weather_table_name,
            hash_key_name=WeathersAttributes.weather_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_weather_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        # ========================= #
        # GET /db/weather/{weather_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=WeathersAttributes.weather_id.name,
            hash_key_value=weather_id,
            table_name=weather_table_name,
            attributesTypesDict=WeathersAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # POST /db/weather/{weather_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=WeathersAttributes.weather_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=weather_table_name,
            attributeTypeDice=WeathersAttributesTypes,
            attributesEnum=WeathersAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # update an agent
        # PUT /db/weather/{weather_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=WeathersAttributes.weather_id.name,
            hash_key_value=weather_id,
            request_body=request_body,
            table_name=weather_table_name,
            attributesTypeDict=WeathersAttributesTypes,
            attributesEnum=WeathersAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        # if exists, delete it
        # ========================= #
        # delete an agent
        # DELETE /db/agent/{agent_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=WeathersAttributes.weather_id.name, hash_key_value=weather_id, table_name=weather_table_name, dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
