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
from common_utils import respond, TESSError, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb, handle_query_items_from_dynamodb, match_path
dynamodb_client = boto3.client('dynamodb')
resources_table_name = os.environ.get("RESOURCES_TABLE_NAME", None)
resources_table_status_valid_at_gsi = os.environ.get(
    "RESOURCES_TABLE_STATUS_VALID_AT_GSI", None)
environment_variables_list = []
environment_variables_list.append(resources_table_name)
environment_variables_list.append(resources_table_status_valid_at_gsi)


class ResourcesAttributes(Enum):
    resource_id = 'resource_id'
    resource_status = 'status'
    resource_name = 'name'
    valid_at = 'valid_at'


ResourcesAttributesTypes = {
    ResourcesAttributes.resource_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ResourcesAttributes.resource_status.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    ResourcesAttributes.resource_name.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    ResourcesAttributes.valid_at.value: {
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
            return respond(err=TESSError("path is missing"))

        if match_path(path=path, route_key=ResourcesRouteKeys.resources.value):
            return handle_resources_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resource.value):
            return handle_resource_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resources_query.value):
            return handle_resources_query_route(event=event, context=context)
        elif match_path(path=path, route_key=ResourcesRouteKeys.resources_scan.value):
            return handle_resources_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

# =================================================================================================
# Resources /db/resources
# =================================================================================================


def handle_resources_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(res_message="message")
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
        return respond(err=TESSError("http method is not supported"))


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

# shared layer


class QueryStringParametersOfScan(Enum):
    key_name = 'key_name'
    key_value = 'key_value'
    key_type = 'key_type'


def handle_scan_items_from_dynamodb(
    query_string_parameters: dict,
    table_name: str,
    dynamodb_client,
    attributes_types_dict: dict,
):
    key_name = query_string_parameters.get(
        QueryStringParametersOfScan.key_name.value, None)
    key_value = query_string_parameters.get(
        QueryStringParametersOfScan.key_value.value, None)
    key_type = query_string_parameters.get(
        QueryStringParametersOfScan.key_type.value, None)
    if key_name is None or key_value is None:
        raise Exception(
            f"key_name, key_value are required for scan action")
    # check if key_name is valid
    if key_name not in attributes_types_dict:
        raise Exception(
            f"key_name {key_name} is not valid")
    # check if key_type is valid
    if key_type is not None and key_type not in attributes_types_dict[key_name]['dynamodb_type']:
        raise Exception(f"key_type {key_type} is not valid")
    # default key_type to string
    if key_type is None:
        key_type = 'S'
    # perform scan
    items = asyncio.run(
        scan_dynamodb_table_with_pagination(
            key_name=key_name,
            key_value=key_value,
            key_type=key_type,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=attributes_types_dict,
        ))
    # items = {"key_name": key_name, "key_value": key_value}
    return respond(res_data=items)


async def scan_dynamodb_table_with_pagination(key_name: str = None,
                                              key_value: str = None,
                                              key_type: str = 'S',
                                              page_size: int = 100,
                                              start_key: str = None,
                                              table_name: str = None,
                                              dynamodb_client: boto3.client = None,
                                              attributes_types_dict: dict = None):
    """
    Scan all items from dynamodb table with pagination with key that is nor primary key or global secondary index
    params: key_name: name of key
    params: key_value: value of key
    params: key_type: type of key
    """
    # Define the parameters for the scan
    if key_name is None or key_value is None:
        raise Exception('key_name or key_value is required')
    table_name = table_name
    filter_expression = f'{key_name} = :id'
    expression_attribute_values = {
        ':id': {key_type: str(key_value)}
    }

    # Create an empty list to store the matching items
    items = []

    # Set the initial parameters for the scan
    scan_params = {
        'TableName': table_name,
        'FilterExpression': filter_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'Limit': page_size,
        'Select': 'ALL_ATTRIBUTES'
    }

    # If there is a start key from a previous scan, use it to resume the scan
    if start_key:
        scan_params['ExclusiveStartKey'] = start_key

    # Scan the table until there are no more items to retrieve
    while True:
        # Execute the scan with the current parameters
        response = await asyncio.to_thread(dynamodb_client.scan, **scan_params)

        # convert dynamodb data to json format
        for item in response.get('Items', []):
            item_dict = deserializer_dynamodb_data_to_json_format(
                item=item,
                attributesTypes=attributes_types_dict
            )
            items.append(item_dict)
        # Check if there are more items to retrieve
        if 'LastEvaluatedKey' in response:
            # If there are more items, update the start key and continue scanning
            start_key = response['LastEvaluatedKey']
            scan_params['ExclusiveStartKey'] = start_key
        else:
            # If there are no more items, stop scanning and return the result list
            break

    return items


def deserializer_dynamodb_data_to_json_format(
        item: dict,
        attributesTypes: dict):
    boto3.resource('dynamodb')
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    decimal_data = {k: deserializer.deserialize(
        v) for k, v in item.items()}
    # covert decimal to float
    str_data = json.dumps(
        decimal_data, default=decimal_default)
    json_data = json.loads(str_data)
    # convert the value to correct type
    for key, value in attributesTypes.items():
        return_type = value.get('return_type', None)
        if return_type is None:
            raise KeyError(
                f"  {key}  missing return type {value}")
        if return_type == ReturnTypes.integer.value:
            json_data[key] = int(json_data[key])

    return json_data


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class ReturnTypes(Enum):
    string = 'string'
    integer = 'integer'
    float = 'float'
    boolean = 'boolean'
