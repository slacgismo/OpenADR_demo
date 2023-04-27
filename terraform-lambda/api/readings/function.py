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
# readings_table_name = os.environ["READINGS_TABLE_NAME"]
# readings_table_meter_id_gsi = os.environ["READINGS_TABLE_METER_ID_GSI"]
# readings_table_meter_id_valid_at_gsi = os.environ["READINGS_TABLE_METER_ID_VALID_AT_GSI"]
readings_table_name = os.environ.get("READINGS_TABLE_NAME", None)
readings_table_meter_id_gsi = os.environ.get(
    "READINGS_TABLE_METER_ID_GSI", None)
readings_table_meter_id_valid_at_gsi = os.environ.get(
    "READINGS_TABLE_METER_ID_VALID_AT_GSI", None)


environment_variables_list = []
environment_variables_list.append(readings_table_name)
environment_variables_list.append(readings_table_meter_id_gsi)
environment_variables_list.append(readings_table_meter_id_valid_at_gsi)


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
    readings_query = "readings/query"
    readings_scan = "readings/scan"

#


def handler(event, context):
    try:
        # check the environment variables
        if None in environment_variables_list:
            raise Exception(
                f"environment variables are not set :{environment_variables_list}")

        # parse the path
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        if match_path(path=path, route_key=ReadingsRouteKeys.readings.value):
            return handle_readings_route(event=event, context=context)
        elif match_path(path=path, route_key=ReadingsRouteKeys.reading.value):
            return handle_reading_route(event=event, context=context)
        elif match_path(path=path, route_key=ReadingsRouteKeys.readings_query.value):
            return handle_readings_query_route(event=event, context=context)
        elif match_path(path=path, route_key=ReadingsRouteKeys.readings_scan.value):
            return handle_readings_scan_route(event=event, context=context)
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
        # GET /db/reading/{reading_id}
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


# ========================= #
# query an reading
# GET /db/reading/query
# ========================= #


def handle_readings_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=readings_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=ReadingsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an reading
# GET /db/reading/scans
# ========================= #


def handle_readings_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=readings_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=ReadingsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
