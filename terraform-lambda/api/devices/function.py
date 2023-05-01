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

devices_table_name = os.environ.get("DEVICES_TABLE_NAME", None)
devices_table_device_id_valid_at_gsi = os.environ.get(
    "DEVICES_TABLE_AGENT_ID_VALID_AT_GSI", None)
devices_table_status_valid_at_gsi = os.environ.get(
    "DEVICES_TABLE_STATUS_VALID_AT_GSI", None)
boto3.resource('dynamodb')


environment_variables_list = []
environment_variables_list.append(devices_table_name)
environment_variables_list.append(devices_table_device_id_valid_at_gsi)
environment_variables_list.append(devices_table_status_valid_at_gsi)


class DevicesAttributes(Enum):
    device_id = 'device_id'
    agent_id = 'agent_id'
    device_type = 'device_type'
    device_model = 'device_model'
    flexible = 'flexible'
    device_status = 'device_status'
    valid_at = 'valid_at'


DevicesAttributesTypes = {
    DevicesAttributes.device_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.agent_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.device_type.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.device_model.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    DevicesAttributes.flexible.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DevicesAttributes.device_status.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    DevicesAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class DevicesRouteKeys(Enum):
    devices = "devices"
    device = "device"
    devices_query = "devices/query"
    devices_scan = "devices/scan"


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

        if match_path(path=path, route_key=DevicesRouteKeys.devices.value):
            return handle_devices_route(event=event, context=context)
        elif match_path(path=path, route_key=DevicesRouteKeys.device.value):
            return handle_device_route(event=event, context=context)
        elif match_path(path=path, route_key=DevicesRouteKeys.devices_query.value):
            return handle_devices_query_route(event=event, context=context)
        elif match_path(path=path, route_key=DevicesRouteKeys.devices_scan.value):
            return handle_devices_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))


# =================================================================================================
# Devices /db/devices
# =================================================================================================


def handle_devices_route(event, context):
    http_method = event['httpMethod']

    if http_method == HTTPMethods.POST.value:
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
        # create a new device
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
        # update an device
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
        return respond(err=TESSError("http method is not supported"))


def handle_devices_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=devices_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=DevicesAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an device
# GET /db/device/scans
# ========================= #


def handle_devices_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=devices_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=DevicesAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
