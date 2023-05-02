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
from common_utils import respond, TESSError, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb, match_path, handle_scan_items_from_dynamodb, handle_query_items_from_dynamodb
dynamodb_client = boto3.client('dynamodb')
resources_table_name = os.environ.get("RESOURCES_TABLE_NAME", None)
resources_table_status_valid_at_gsi = os.environ.get(
    "RESOURCES_TABLE_STATUS_VALID_AT_GSI", None)
environment_variables_list = []
environment_variables_list.append(resources_table_name)
environment_variables_list.append(resources_table_status_valid_at_gsi)


class ResourcesAttributes(Enum):
    resource_id = 'resource_id'
    resource_status = 'resource_status'
    resource_name = 'resource_name'
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


# class QueryStringParametersOfQuery(Enum):
#     gsi_name = 'gsi_name'
#     key_value = 'key_value'
#     key_name = 'key_name'
#     key_type = 'key_type'
#     range_key = 'range_key'
#     range_key_value = 'range_key_value'
#     range_key_type = 'range_key_type'
#     start_from = 'start_from'
#     end_at = 'end_at'


# def handle_query_items_from_dynamodb(
#     query_string_parameters: dict,
#     table_name: str,
#     environment_variables_list: set,
#     dynamodb_client: boto3.client,
#     attributes_types_dict: dict,

# ):

#     gsi_name = query_string_parameters.get(
#         QueryStringParametersOfQuery.gsi_name.value, None)
#     key_value = query_string_parameters.get(
#         QueryStringParametersOfQuery.key_value.value, None)
#     key_name = query_string_parameters.get(
#         QueryStringParametersOfQuery.key_name.value, None)
#     if gsi_name is None or key_value is None or key_name is None:
#         raise Exception(
#             f"gsi_name, key_value, key_name are required for query action")

#     key_type = query_string_parameters.get(
#         QueryStringParametersOfQuery.key_type.value, None)
#     range_key = query_string_parameters.get(
#         QueryStringParametersOfQuery.range_key.value, None)
#     range_key_type = query_string_parameters.get(
#         QueryStringParametersOfQuery.range_key_type.value, None)
#     start_from = query_string_parameters.get(
#         QueryStringParametersOfQuery.start_from.value, None)
#     end_at = query_string_parameters.get(
#         QueryStringParametersOfQuery.end_at.value, None)
#     # check if the key_type is valid
#     if key_type is not None and key_type not in attributes_types_dict[key_name]['dynamodb_type']:
#         raise Exception(f"key_type {key_type} is not valid")
#     # check if the key_name is valid
#     if key_name is not None and key_name not in attributes_types_dict:
#         raise Exception(
#             f"key_name {key_name} is not valid")

#     # check if the range_key is valid
#     if range_key is not None and range_key not in attributes_types_dict:
#         raise Exception(f"range_key {range_key} is not valid")

#     # check if the gsi_name is valid
#     if range_key is not None and range_key_type not in attributes_types_dict[key_name]['dynamodb_type']:
#         raise Exception(f"range_key_type {range_key_type} is not valid")
#     if gsi_name is None or gsi_name not in environment_variables_list:
#         raise Exception(f"gsi_name {gsi_name} is not valid")

#     items = asyncio.run(
#         query_items_from_dynamodb_with_gsi(
#             table_name=table_name,
#             dynamodb_client=dynamodb_client,
#             gsi_name=gsi_name,
#             key_value=key_value,
#             key_name=key_name,
#             key_type=key_type,
#             range_key=range_key,
#             range_key_type=range_key_type,
#             start_from=start_from,
#             end_at=end_at,
#             attributes_types_dict=attributes_types_dict
#         )
#     )

#     return respond(res_data=items)


# async def query_items_from_dynamodb_with_gsi(
#         table_name: str = None,
#         gsi_name: str = None,
#         key_value: str = None,
#         key_name: str = None,
#         key_type: str = 'S',
#         dynamodb_client: boto3.client = None,
#         page_size: int = 25,
#         range_key: str = None,
#         range_key_type: str = 'N',
#         start_from: str = None,
#         end_at: str = None,
#         attributes_types_dict: dict = None,
# ):
#     """
#     Query items from dynamodb with global secondary index
#     if range_key is not None, query items with range key
#         if start_from is not None, and end_at is None, query items from start_from to end
#         if start_from is None, and end_at is not None, query items from start to end_at
#         if start_from is not None, and end_at is not None, query items from start_from to end_at
#     params: table_name: name of table
#     params: gsi_name: name of global secondary index
#     params: key_value: value of key (hash key value of global secondary index)
#     params: key_name: name of key (hash key name of global secondary index)
#     params: key_type: type of key (hash key type of global secondary index)
#     params: dynamodb_client: dynamodb client
#     params: page_size: number of items per page
#     params: range_key: name of range key
#     params: range_key_type: type of range key
#     params: start_from: start from range key value
#     params: end_at: end at range key value
#     return: list of items
#     """
#     try:
#         items = []
#         last_evaluated_key = None
#         # condition_expression = f"{hash_key} = :{hash_key}"
#         if gsi_name is None:
#             key_condition_expression = f"{key_name} = :{key_name}"
#             expression_attribute_values = {
#                 f':{key_name}': {key_type: key_value}}
#         elif start_from is None and end_at is None:
#             key_condition_expression = f"{key_name} = :{key_name}"
#             expression_attribute_values = {
#                 f':{key_name}': {key_type: key_value}}
#         elif start_from is None and end_at is not None:
#             key_condition_expression = f"{key_name} = :{key_name} AND {range_key} <= :end_at"
#             expression_attribute_values = {
#                 f':{key_name}': {key_type: key_name},
#                 ':end_at': {range_key_type: str(end_at)}
#             }
#         elif start_from is not None and end_at is None:
#             key_condition_expression = f"{key_name} = :{key_name} AND {range_key} >= :start_from"
#             expression_attribute_values = {
#                 f':{key_name}': {key_type: key_value},
#                 ':start_from': {range_key_type: str(start_from)}
#             }
#         else:
#             key_condition_expression = f"{key_name} = :{key_name} AND {range_key} BETWEEN :start_from AND :end_at"
#             expression_attribute_values = {
#                 f':{key_name}': {key_type: key_value},
#                 ':start_from': {range_key_type: str(start_from)},
#                 ':end_at': {range_key_type: str(end_at)}
#             }
#         # perform pagination
#         print(
#             "----------------- start query items from dynamodb with gsi -----------------")
#         print(f"key_condition_expression {key_condition_expression}")
#         print(f"expression_attribute_values {expression_attribute_values}")
#         while True:
#             pagination_params = {
#                 'TableName': table_name,
#                 'IndexName': gsi_name,
#                 'KeyConditionExpression': key_condition_expression,
#                 'ExpressionAttributeValues': expression_attribute_values,
#                 'ReturnConsumedCapacity': 'TOTAL',
#                 'Limit': page_size,
#             }
#             if last_evaluated_key:
#                 pagination_params['ExclusiveStartKey'] = last_evaluated_key

#             response = await asyncio.to_thread(dynamodb_client.query, **pagination_params)

#             # convert dynamodb data to json format
#             for item in response.get('Items', []):
#                 item_dict = deserializer_dynamodb_data_to_json_format(
#                     item=item, attributesTypes=attributes_types_dict)
#                 items.append(item_dict)
#                 # for key, value in item.items():
#                 #     item_dict[key] = value.get('S', value.get('N'))
#                 # items.append(item_dict)

#             if 'LastEvaluatedKey' in response and response['LastEvaluatedKey']:
#                 last_evaluated_key = response['LastEvaluatedKey']
#             else:
#                 break

#         return items
#     except Exception as e:
#         raise Exception(str(e))


# def deserializer_dynamodb_data_to_json_format(
#         item: dict,
#         attributesTypes: dict):
#     boto3.resource('dynamodb')
#     deserializer = boto3.dynamodb.types.TypeDeserializer()
#     decimal_data = {k: deserializer.deserialize(
#         v) for k, v in item.items()}
#     # covert decimal to float
#     str_data = json.dumps(
#         decimal_data, default=decimal_default)
#     json_data = json.loads(str_data)
#     # convert the value to correct type
#     for key, value in attributesTypes.items():
#         return_type = value.get('return_type', None)
#         if return_type is None:
#             raise KeyError(
#                 f"  {key}  missing return type {value}")
#         if return_type == ReturnTypes.integer.value:
#             json_data[key] = int(json_data[key])

#     return json_data


# def decimal_default(obj):
#     if isinstance(obj, Decimal):
#         return float(obj)
#     raise TypeError


# class ReturnTypes(Enum):
#     string = 'string'
#     integer = 'integer'
#     float = 'float'
#     boolean = 'boolean'
