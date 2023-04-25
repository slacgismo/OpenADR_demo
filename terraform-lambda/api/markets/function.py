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

        return post_list_of_markets_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=markets_table_name
        )
    elif http_method == HTTPMethods.PUT.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return put_list_of_markets_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=markets_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_markets_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=markets_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_markets_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="post list of markets to dynamodb")


def put_list_of_markets_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    return respond(err=None, res="put list of markets to dynamodb")


def delete_list_of_markets_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    return respond(err=None, res="delete list of markets from dynamodb")
    # =================================================================================================
    # Agent /db/market/{market_id}
    # =================================================================================================


def handle_market_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        return handle_get_market_from_market_id(
            market_id=market_id, dynamodb_client=dynamodb_client, table_name=markets_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_market(request_body=request_body, table_name=markets_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_market(market_id=market_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        return handle_delete_market(market_id=market_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/market/{market_id}
# ========================= #


def handle_get_market_from_market_id(market_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=market_id,
                key=MarketsAttributes.market_id.name,
                table_name=markets_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            market_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=MarketsAttributesTypes)
            return respond(err=None, res=market_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new market
# POST /db/market/{market_id}
# ========================= #

def handle_post_market(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        # create a new market
        market_id = str(guid())
        item = create_item(
            primary_key_name=MarketsAttributes.market_id.name,
            primary_key_value=market_id,
            request_body=request_body,
            attributeType=MarketsAttributesTypes,
            attributes=MarketsAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post an market to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an market
# PUT /db/market/{market_id}
# ========================= #


def handle_put_market(market_id: str, request_body: dict, table_name: str = markets_table_name, dynamodb_client: boto3.client = dynamodb_client):
    if market_id is None:
        raise KeyError("market_id is missing")
    try:
        # check if market_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=market_id,
                key=MarketsAttributes.market_id.name,
                table_name=markets_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"market_id {market_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=MarketsAttributes.market_id.name,
                primary_key_value=market_id,
                request_body=request_body,
                attributeType=MarketsAttributesTypes,
                attributes=MarketsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an market to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an market
# DELETE /db/market/{market_id}
# ========================= #


def handle_delete_market(market_id: str):
    try:
        # check if market_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=market_id,
                key=MarketsAttributes.market_id.name,
                table_name=markets_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=MarketsAttributes.market_id.name,
                id=market_id,
                table_name=markets_table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
