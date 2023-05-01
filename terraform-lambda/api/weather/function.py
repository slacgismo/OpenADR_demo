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
weather_table_name = os.environ.get("WEATHER_TABLE_NAME", None)
weather_table_zip_code_valid_at_gsi = os.environ.get(
    "WEATHER_TABLE_ZIP_CODE_VALID_AT_GSI", None)

environment_variables_list = []
environment_variables_list.append(weather_table_name)
environment_variables_list.append(weather_table_zip_code_valid_at_gsi)


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
    WeathersAttributes.weather_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    WeathersAttributes.zip_code.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    WeathersAttributes.temperature.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.humidity.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.solar.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.wind_speed.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    WeathersAttributes.wind_direction.value: {
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
    weathers_query = "weathers/query"
    weathers_scan = "weathers/scan"


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

        if match_path(path=path, route_key=WeathersRouteKeys.weathers.value):
            return handle_weathers_route(event=event, context=context)
        elif match_path(path=path, route_key=WeathersRouteKeys.weather.value):
            return handle_weather_route(event=event, context=context)
        elif match_path(path=path, route_key=WeathersRouteKeys.weathers_query.value):
            return handle_weathers_query_route(event=event, context=context)
        elif match_path(path=path, route_key=WeathersRouteKeys.weathers_scan.value):
            return handle_weathers_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))


# =================================================================================================
# Weathers /db/weathers
# =================================================================================================


def handle_weathers_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

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
        # update an weather
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
        # delete an weather
        # DELETE /db/weather/{weather_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=WeathersAttributes.weather_id.name, hash_key_value=weather_id, table_name=weather_table_name, dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))
# ========================= #
# query an weather
# GET /db/weather/query
# ========================= #


def handle_weathers_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=weather_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=WeathersAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an weather
# GET /db/weather/scans
# ========================= #


def handle_weathers_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=weather_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=WeathersAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
