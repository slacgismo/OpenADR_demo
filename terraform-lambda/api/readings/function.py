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

        return post_list_of_readings_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=readings_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_readings_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=readings_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_readings_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=readings_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_readings_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of readings to dynamodb")


def put_list_of_readings_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of readings to dynamodb")


def delete_list_of_readings_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of readings from dynamodb")
    # =================================================================================================
    # Agent /db/reading/{reading_id}
    # =================================================================================================


def handle_reading_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        return handle_get_reading_from_reading_id(
            reading_id=reading_id, dynamodb_client=dynamodb_client, table_name=readings_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_reading(request_body=request_body, table_name=readings_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_reading(reading_id=reading_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'reading_id' not in event['pathParameters']:
            raise KeyError("reading_id is missing")
        reading_id = event['pathParameters']['reading_id']
        return handle_delete_reading(reading_id=reading_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/reading/{reading_id}
# ========================= #


def handle_get_reading_from_reading_id(reading_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=reading_id,
                key=ReadingsAttributes.reading_id.name,
                table_name=readings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            reading_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=ReadingsAttributesTypes)
            return respond(err=None, res=reading_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new reading
# POST /db/reading/{reading_id}
# ========================= #

def handle_post_reading(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new reading
        reading_id = str(guid())
        item = create_item(
            primary_key_name=ReadingsAttributes.reading_id.name,
            primary_key_value=reading_id,
            request_body=request_body,
            attributeType=ReadingsAttributesTypes,
            attributes=ReadingsAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an reading to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an reading
# PUT /db/reading/{reading_id}
# ========================= #


def handle_put_reading(reading_id: str, request_body: dict, table_name: str = readings_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if reading_id is None:
        raise KeyError("reading_id is missing")
    try:
        # check if reading_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=reading_id,
                key=ReadingsAttributes.reading_id.name,
                table_name=readings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"reading_id {reading_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=ReadingsAttributes.reading_id.name,
                primary_key_value=reading_id,
                request_body=request_body,
                attributeType=ReadingsAttributesTypes,
                attributes=ReadingsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an reading to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an reading
# DELETE /db/reading/{reading_id}
# ========================= #


def handle_delete_reading(reading_id: str):
    try:
        # check if reading_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=reading_id,
                key=ReadingsAttributes.reading_id.name,
                table_name=readings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=ReadingsAttributes.reading_id.name,
                id=reading_id,
                table_name=readings_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
