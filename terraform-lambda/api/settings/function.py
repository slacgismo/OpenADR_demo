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
settings_table_name = os.environ["SETTINGS_TABLE_NAME"]

boto3.resource('dynamodb')


class SettingsAttributes(Enum):
    setting_id = 'setting_id'
    device_id = 'device_id'
    name = 'name'
    value = 'value'
    valid_at = 'valid_at'


SettingsAttributesTypes = {
    SettingsAttributes.setting_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.device_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.name.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.value.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    SettingsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class SettingsRouteKeys(Enum):
    settings = "settings"
    setting = "setting"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == SettingsRouteKeys.settings.value:
            return handle_settings_route(event=event, context=context)
        elif route_key == SettingsRouteKeys.setting.value:
            return handle_setting_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Settings /db/settings
# =================================================================================================


def handle_settings_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of settings from setting id")
    elif http_method == HTTPMethods.POST.value:

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
        # update an agent
        # PUT /db/agent/{agent_id}
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
        return respond(err=TESSError("http method is not supported"), res=None)
