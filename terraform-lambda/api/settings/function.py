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

        return post_list_of_settings_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settings_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_settings_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settings_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_settings_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=settings_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_settings_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of settings to dynamodb")


def put_list_of_settings_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of settings to dynamodb")


def delete_list_of_settings_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of settings from dynamodb")
    # =================================================================================================
    # Agent /db/setting/{setting_id}
    # =================================================================================================


def handle_setting_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        return handle_get_setting_from_setting_id(
            setting_id=setting_id, dynamodb_client=dynamodb_client, table_name=settings_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_setting(request_body=request_body, table_name=settings_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_setting(setting_id=setting_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'setting_id' not in event['pathParameters']:
            raise KeyError("setting_id is missing")
        setting_id = event['pathParameters']['setting_id']
        return handle_delete_setting(setting_id=setting_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/setting/{setting_id}
# ========================= #


def handle_get_setting_from_setting_id(setting_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=setting_id,
                key=SettingsAttributes.setting_id.name,
                table_name=settings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            setting_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=SettingsAttributesTypes)
            return respond(err=None, res=setting_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new setting
# POST /db/setting/{setting_id}
# ========================= #

def handle_post_setting(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new setting
        setting_id = str(guid())
        item = create_item(
            primary_key_name=SettingsAttributes.setting_id.name,
            primary_key_value=setting_id,
            request_body=request_body,
            attributeType=SettingsAttributesTypes,
            attributes=SettingsAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an setting to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an setting
# PUT /db/setting/{setting_id}
# ========================= #


def handle_put_setting(setting_id: str, request_body: dict, table_name: str = settings_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if setting_id is None:
        raise KeyError("setting_id is missing")
    try:
        # check if setting_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=setting_id,
                key=SettingsAttributes.setting_id.name,
                table_name=settings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"setting_id {setting_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=SettingsAttributes.setting_id.name,
                primary_key_value=setting_id,
                request_body=request_body,
                attributeType=SettingsAttributesTypes,
                attributes=SettingsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an setting to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an setting
# DELETE /db/setting/{setting_id}
# ========================= #


def handle_delete_setting(setting_id: str):
    try:
        # check if setting_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=setting_id,
                key=SettingsAttributes.setting_id.name,
                table_name=settings_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=SettingsAttributes.setting_id.name,
                id=setting_id,
                table_name=settings_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
