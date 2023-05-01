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
settings_table_name = os.environ.get("SETTINGS_TABLE_NAME", None)
settings_table_device_id_valid_at_gsi = os.environ.get(
    "SETTINGS_TABLE_DEVICE_ID_VALID_AT_GSI", None)


environment_variables_list = []
environment_variables_list.append(settings_table_name)
environment_variables_list.append(settings_table_device_id_valid_at_gsi)


class SettingsAttributes(Enum):
    setting_id = 'setting_id'
    device_id = 'device_id'
    setting_name = 'name'
    setting_value = 'value'
    valid_at = 'valid_at'


SettingsAttributesTypes = {
    SettingsAttributes.setting_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.device_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.setting_name.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.setting_value.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class SettingsRouteKeys(Enum):
    settings = "settings"
    setting = "setting"
    settings_query = "settings/query"
    settings_scan = "settings/scan"


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

        if match_path(path=path, route_key=SettingsRouteKeys.settings.value):
            return handle_settings_route(event=event, context=context)
        elif match_path(path=path, route_key=SettingsRouteKeys.setting.value):
            return handle_setting_route(event=event, context=context)
        elif match_path(path=path, route_key=SettingsRouteKeys.settings_query.value):
            return handle_settings_query_route(event=event, context=context)
        elif match_path(path=path, route_key=SettingsRouteKeys.settings_scan.value):
            return handle_settings_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

# =================================================================================================
# Settings /db/settings
# =================================================================================================


def handle_settings_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=settings_table_name,
            hash_key_name=SettingsAttributes.setting_id.name,
            attributesTypeDict=SettingsAttributesTypes
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=settings_table_name,
            hash_key_name=SettingsAttributes.setting_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_setting_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        # ========================= #
        # GET /db/setting/{setting_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=SettingsAttributes.setting_id.name,
            hash_key_value=setting_id,
            table_name=settings_table_name,
            attributesTypesDict=SettingsAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # POST /db/setting/{setting_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=SettingsAttributes.setting_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=settings_table_name,
            attributeTypeDice=SettingsAttributesTypes,
            attributesEnum=SettingsAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # update an setting
        # PUT /db/setting/{setting_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=SettingsAttributes.setting_id.name,
            hash_key_value=setting_id,
            request_body=request_body,
            table_name=settings_table_name,
            attributesTypeDict=SettingsAttributesTypes,
            attributesEnum=SettingsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        # ========================= #
        # DELETE /db/setting/{setting_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=SettingsAttributes.setting_id.name,
            hash_key_value=setting_id,
            table_name=settings_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))


# ========================= #
# query an setting
# GET /db/setting/query
# ========================= #


def handle_settings_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=settings_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=SettingsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an setting
# GET /db/setting/scans
# ========================= #


def handle_settings_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=settings_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=SettingsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
