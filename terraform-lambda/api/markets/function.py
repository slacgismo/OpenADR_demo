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
markets_table_name = os.environ["MARKETS_TABLE_NAME"]
markets_table_resource_id_valid_at_gsi = os.environ["MARKETS_TABLE_RESOURCE_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class MarketsAttributes(Enum):
    market_id = 'market_id'
    name = 'name'
    resource_id = 'resource_id'
    units = 'units'
    interval = 'interval'
    status = 'status'
    valid_at = 'valid_at'


MarketsAttributesTypes = {
    MarketsAttributes.market_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.name.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.units.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    MarketsAttributes.interval.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MarketsAttributes.status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    MarketsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class MarketsRouteKeys(Enum):
    markets = "markets"
    market = "market"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == MarketsRouteKeys.markets.value:
            return handle_markets_route(event=event, context=context)
        elif route_key == MarketsRouteKeys.market.value:
            return handle_market_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Markets /db/markets
# =================================================================================================


def handle_markets_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of markets from resource id")
    elif http_method == HTTPMethods.POST.value:

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
        # create a new agent
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
        # update an agent
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
        # delete an agent
        # DELETE /db/market/{market_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=MarketsAttributes.market_id.name,
            hash_key_value=market_id,
            table_name=markets_table_name,
            dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
