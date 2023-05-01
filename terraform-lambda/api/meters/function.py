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

meters_table_name = os.environ.get("METERS_TABLE_NAME", None)
meters_table_resource_id_device_id_gsi = os.environ.get(
    "METERS_TABLE_RESOURCE_ID_DEVICE_ID_GSI", None)

environment_variables_list = []
environment_variables_list.append(meters_table_name)
environment_variables_list.append(meters_table_resource_id_device_id_gsi)


class MetersAttributes(Enum):
    meter_id = 'meter_id'
    device_id = 'device_id'
    resource_id = 'resource_id'
    metere_status = 'status'
    valid_at = 'valid_at'


MetersAttributesTypes = {
    MetersAttributes.meter_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.device_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.resource_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MetersAttributes.metere_status.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MetersAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class MetersRouteKeys(Enum):
    meters = "meters"
    meter = "meter"
    meters_query = "meters/query"
    meters_scan = "meters/scan"


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

        if match_path(path=path, route_key=MetersRouteKeys.meters.value):
            return handle_meters_route(event=event, context=context)
        elif match_path(path=path, route_key=MetersRouteKeys.meter.value):
            return handle_meter_route(event=event, context=context)
        elif match_path(path=path, route_key=MetersRouteKeys.meters_query.value):
            return handle_meters_query_route(event=event, context=context)
        elif match_path(path=path, route_key=MetersRouteKeys.meters_scan.value):
            return handle_meters_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))
# =================================================================================================
# Meters /db/meters
# =================================================================================================


def handle_meters_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

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
        # GET /db/meter/{meter_id}
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
        # create a new meter
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
        # update an meter
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
        # delete an meter
        # DELETE  /db/meter/{meter_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=MetersAttributes.meter_id.name,
            hash_key_value=meter_id,
            table_name=meters_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))


# ========================= #
# query an meter
# GET /db/meter/query
# ========================= #


def handle_meters_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=meters_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=MetersAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an meter
# GET /db/meter/scans
# ========================= #


def handle_meters_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=meters_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=MetersAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
