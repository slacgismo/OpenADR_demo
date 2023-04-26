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

        return post_list_of_weathers_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=weather_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_weathers_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=weather_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_weathers_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=weather_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_weathers_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of weathers to dynamodb")


def put_list_of_weathers_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of weathers to dynamodb")


def delete_list_of_weathers_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of weathers from dynamodb")
    # =================================================================================================
    # Agent /db/weather/{weather_id}
    # =================================================================================================


def handle_weather_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        return handle_get_weather_from_weather_id(
            weather_id=weather_id, dynamodb_client=dynamodb_client, table_name=weather_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_weather(request_body=request_body, table_name=weather_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_weather(weather_id=weather_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'weather_id' not in event['pathParameters']:
            raise KeyError("weather_id is missing")
        weather_id = event['pathParameters']['weather_id']
        return handle_delete_weather(weather_id=weather_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/weather/{weather_id}
# ========================= #


def handle_get_weather_from_weather_id(weather_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=weather_id,
                key=WeathersAttributes.weather_id.name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            weather_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=WeathersAttributesTypes)
            return respond(err=None, res=weather_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new weather
# POST /db/weather/{weather_id}
# ========================= #

def handle_post_weather(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new weather
        weather_id = str(guid())
        item = create_item(
            primary_key_name=WeathersAttributes.weather_id.name,
            primary_key_value=weather_id,
            request_body=request_body,
            attributeType=WeathersAttributesTypes,
            attributes=WeathersAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an weather to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an weather
# PUT /db/weather/{weather_id}
# ========================= #


def handle_put_weather(weather_id: str, request_body: dict, table_name: str = weather_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if weather_id is None:
        raise KeyError("weather_id is missing")
    try:
        # check if weather_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=weather_id,
                key=WeathersAttributes.weather_id.name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"weather_id {weather_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=WeathersAttributes.weather_id.name,
                primary_key_value=weather_id,
                request_body=request_body,
                attributeType=WeathersAttributesTypes,
                attributes=WeathersAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an weather to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an weather
# DELETE /db/weather/{weather_id}
# ========================= #


def handle_delete_weather(weather_id: str):
    try:
        # check if weather_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=weather_id,
                key=WeathersAttributes.weather_id.name,
                table_name=weather_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=WeathersAttributes.weather_id.name,
                id=weather_id,
                table_name=weather_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))


def handle_delete_agent(
        hash_key_value: str = None,
        hash_key_name: str = None,
        table_name: str = None,
        dynamodb_client: boto3.client = dynamodb_client):
    try:
        # check if agent_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=hash_key_value,
                key=hash_key_name
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=AgentsAttributes.agent_id.name,
                id=hash_key_value,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
