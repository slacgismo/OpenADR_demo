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
resources_table_name = os.environ.get("RESOURCES_TABLE_NAME", None)

environment_variables_list = []
environment_variables_list.append(resources_table_name)


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
    resources_query = "resources/query"
    resources_scan = "resources/scan"


# =================================================================================================
# Main handler
# =================================================================================================

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

        if match_path(path=path, route_key=ResourcesRouteKeys.resources.value):
            return handle_resources_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resource.value):
            return handle_resource_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resources_query.value):
            return handle_resources_query_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resources_scan.value):
            return handle_resources_scan_route(event=event, context=context)
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

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=resources_table_name,
            hash_key_name=ResourcesAttributes.resource_id.name,
            attributesTypeDict=ResourcesAttributesTypes,
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=resources_table_name,
            hash_key_name=ResourcesAttributes.resource_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_resource_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        # ========================= #
        # GET /db/resource/{resource_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=ResourcesAttributes.resource_id.name,
            hash_key_value=resource_id,
            table_name=resources_table_name,
            attributesTypesDict=ResourcesAttributesTypes,
            dynamodb_client=dynamodb_client
        )

    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # POST /db/resource/{resource_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=ResourcesAttributes.resource_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=resources_table_name,
            attributeTypeDice=ResourcesAttributesTypes,
            attributesEnum=ResourcesAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # PUT /db/resource/{resource_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=ResourcesAttributes.resource_id.name,
            hash_key_value=resource_id,
            request_body=request_body,
            table_name=resources_table_name,
            attributesTypeDict=ResourcesAttributesTypes,
            attributesEnum=ResourcesAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'resource_id' not in event['pathParameters']:
            raise KeyError("resource_id is missing")
        resource_id = event['pathParameters']['resource_id']
        # ========================= #
        # DELETE /db/resource/{resource_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=ResourcesAttributes.resource_id.name,
            hash_key_value=resource_id,
            table_name=resources_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)


# ========================= #
# query an resource
# GET /db/resource/query
# ========================= #


def handle_resources_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=resources_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=ResourcesAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an resource
# GET /db/resource/scans
# ========================= #


def handle_resources_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=resources_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=ResourcesAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
