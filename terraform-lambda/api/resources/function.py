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
resources_table_name = os.environ["RESOURCES_TABLE_NAME"]

boto3.resource('dynamodb')


class ResourcesAttributes(Enum):
    resource_id = 'resource_id'
    status = 'status'
    name = 'name'
    valid_at = 'valid_at'


ResourcesAttributesTypes = {
    ResourcesAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ResourcesAttributes.status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    ResourcesAttributes.name.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ResourcesAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class ResourcesRouteKeys(Enum):
    resources = "resources"
    resource = "resource"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == ResourcesRouteKeys.resources.value:
            return handle_resources_route(event=event, context=context)
        elif route_key == ResourcesRouteKeys.resource.value:
            return handle_resource_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Resources /db/resources
# =================================================================================================


def handle_resources_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of resources from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return post_list_of_resources_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=resources_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_resources_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=resources_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_resources_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=resources_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_resources_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of resources to dynamodb")


def put_list_of_resources_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of resources to dynamodb")


def delete_list_of_resources_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of resources from dynamodb")
    # =================================================================================================
    # Agent /db/resource/{resource_id}
    # =================================================================================================


def handle_resource_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        return handle_get_resource_from_resource_id(
            resource_id=resource_id, dynamodb_client=dynamodb_client, table_name=resources_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_resource(request_body=request_body, table_name=resources_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_resource(resource_id=resource_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        return handle_delete_resource(resource_id=resource_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/resource/{resource_id}
# ========================= #


def handle_get_resource_from_resource_id(resource_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=resource_id,
                key=ResourcesAttributes.resource_id.name,
                table_name=resources_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            resource_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=ResourcesAttributesTypes)
            return respond(err=None, res=resource_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new resource
# POST /db/resource/{resource_id}
# ========================= #

def handle_post_resource(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new resource
        resource_id = str(guid())
        item = create_item(
            primary_key_name=ResourcesAttributes.resource_id.name,
            primary_key_value=resource_id,
            request_body=request_body,
            attributeType=ResourcesAttributesTypes,
            attributes=ResourcesAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an resource to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an resource
# PUT /db/resource/{resource_id}
# ========================= #


def handle_put_resource(resource_id: str, request_body: dict, table_name: str = resources_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if resource_id is None:
        raise KeyError("resource_id is missing")
    try:
        # check if resource_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=resource_id,
                key=ResourcesAttributes.resource_id.name,
                table_name=resources_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"resource_id {resource_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=ResourcesAttributes.resource_id.name,
                primary_key_value=resource_id,
                request_body=request_body,
                attributeType=ResourcesAttributesTypes,
                attributes=ResourcesAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an resource to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an resource
# DELETE /db/resource/{resource_id}
# ========================= #


def handle_delete_resource(resource_id: str):
    try:
        # check if resource_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=resource_id,
                key=ResourcesAttributes.resource_id.name,
                table_name=resources_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=ResourcesAttributes.resource_id.name,
                id=resource_id,
                table_name=resources_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
