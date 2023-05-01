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
markets_table_name = os.environ.get("MARKETS_TABLE_NAME", None)
markets_table_resource_id_valid_at_gsi = os.environ.get(
    "MARKETS_TABLE_RESOURCE_ID_VALID_AT_GSI", None)

# markets_table_name = os.environ["MARKETS_TABLE_NAME"]
# markets_table_resource_id_valid_at_gsi = os.environ["MARKETS_TABLE_RESOURCE_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')

environment_variables_list = []
environment_variables_list.append(markets_table_name)
environment_variables_list.append(markets_table_resource_id_valid_at_gsi)


class MarketsAttributes(Enum):
    market_id = 'market_id'
    market_name = 'name'
    resource_id = 'resource_id'
    units = 'units'
    interval = 'interval'
    market_status = 'market_status'
    valid_at = 'valid_at'


MarketsAttributesTypes = {
    MarketsAttributes.market_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.market_name.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.resource_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.units.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.interval.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MarketsAttributes.market_status.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MarketsAttributes.valid_at.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class MarketsRouteKeys(Enum):
    markets = "markets"
    market = "market"
    markets_query = "markets/query"
    markets_scan = "markets/scan"


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

        if match_path(path=path, route_key=MarketsRouteKeys.markets.value):
            return handle_markets_route(event=event, context=context)
        elif match_path(path=path, route_key=MarketsRouteKeys.market.value):
            return handle_market_route(event=event, context=context)
        elif match_path(path=path, route_key=MarketsRouteKeys.markets_query.value):
            return handle_markets_query_route(event=event, context=context)
        elif match_path(path=path, route_key=MarketsRouteKeys.markets_scan.value):
            return handle_markets_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

# =================================================================================================
# Markets /db/markets
# =================================================================================================


def handle_markets_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=markets_table_name,
            hash_key_name=MarketsAttributes.market_id.name,
            attributesTypeDict=MarketsAttributesTypes,
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=markets_table_name,
            hash_key_name=MarketsAttributes.market_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_market_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        # ========================= #
        # GET /db/market/{market_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=MarketsAttributes.market_id.name,
            hash_key_value=market_id,
            table_name=markets_table_name,
            attributesTypesDict=MarketsAttributesTypes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new market
        # POST /db/market/{market_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=MarketsAttributes.market_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=markets_table_name,
            attributeTypeDice=MarketsAttributesTypes,
            attributesEnum=MarketsAttributes,
            dynamodb_client=dynamodb_client

        )
    elif http_method == HTTPMethods.PUT.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        # ========================= #
        # update an market
        # PUT /db/market/{market_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=MarketsAttributes.market_id.name,
            hash_key_value=market_id,
            request_body=request_body,
            table_name=markets_table_name,
            attributesTypeDict=MarketsAttributesTypes,
            attributesEnum=MarketsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        # ========================= #
        # delete an market
        # DELETE /db/market/{market_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=MarketsAttributes.market_id.name,
            hash_key_value=market_id,
            table_name=markets_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))


# ========================= #
# query an market
# GET /db/market/query
# ========================= #


def handle_markets_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=markets_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=MarketsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an market
# GET /db/market/scans
# ========================= #


def handle_markets_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=markets_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=MarketsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
