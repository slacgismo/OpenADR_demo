import json
import asyncio
import boto3
import json
import time
import os
from enum import Enum
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# cmmmon_utils, constants is from shared layer
from common_utils import respond, TESSError, get_path, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb
dynamodb_client = boto3.client('dynamodb')
auctions_table_name = os.environ["AUCTIONS_TABLE_NAME"]
auctions_table_market_id_valid_at_gsi = os.environ["AUCTIONS_TABLE_MARKET_ID_VALID_AT_GSI"]
boto3.resource('dynamodb')


class AuctionsAttributes(Enum):
    auction_id = 'auction_id'
    market_id = 'market_id'
    clearing_time = 'clearing_time'
    expected_price = 'expected_price'
    expected_stdev = 'expected_stdev'
    reference_price = 'reference_price'
    price = 'price'
    quantity = 'quantity'
    marginal_type = 'marginal_type'
    marginal_order = 'marginal_order'
    marginal_quantity = 'marginal_quantity'
    marginal_rank = 'marginal_rank'
    valid_at = 'valid_at'


AuctionsAttributesTypes = {
    AuctionsAttributes.auction_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.market_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.clearing_time.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AuctionsAttributes.expected_price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.expected_stdev.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.reference_price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.price.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.quantity.name: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.marginal_type.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_order.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_quantity.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.marginal_rank.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


class AgentsRouteKeys(Enum):
    auctions = "auctions"
    auction = "auction"


def handler(event, context):
    try:
        path = event['path']
        if 'path' not in event:
            return respond(err=TESSError("path is missing"), res=None, status_code=400)

        route_key = get_path(path=path, index=3)
        if route_key == AgentsRouteKeys.auctions.value:
            return handle_auctions_route(event=event, context=context)
        elif route_key == AgentsRouteKeys.auction.value:
            return handle_auction_route(event=event, context=context)
        else:
            raise Exception("route key is not supported")

    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)

# =================================================================================================
# Agents /db/auctions
# =================================================================================================


def handle_auctions_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # ========================= #
        # GET /db/auctions
        # ========================= #
        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of auctions from resource id")
    elif http_method == HTTPMethods.POST.value:
        # ========================= #
        # POST /db/auctions
        # ========================= #
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=auctions_table_name,
            hash_key_name=AuctionsAttributes.agent_id.name,
            attributesTypeDict=AuctionsAttributesTypes
        )

    elif http_method == HTTPMethods.DELETE.value:
        # ========================= #
        # DELETE /db/auctions
        # ========================= #
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_items_from_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=auctions_table_name,
            hash_key_name=AuctionsAttributes.auction_id.name,
        )
    else:
        raise Exception("http method is not supported")


def handle_auction_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        # ========================= #
        # GET /db/auction/{auction_id}
        # ========================= #
        return handle_get_item_from_dynamodb_with_hash_key(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=auction_id,
            table_name=auctions_table_name,
            attributesTypesDict=AuctionsAttributesTypes,
            dynamodb_client=dynamodb_client
        )

    elif http_method == HTTPMethods.POST.value:
        # ========================= #
        # POST /db/auction/{auction_id}
        # ========================= #
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_create_item_to_dynamodb(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=auctions_table_name,
            attributeTypeDice=AuctionsAttributesTypes,
            attributesEnum=AuctionsAttributes,
            dynamodb_client=dynamodb_client

        )
        # return handle_post_auction(request_body=request_body, table_name=auctions_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        # ========================= #
        # PUT /db/auction/{auction_id}
        # ========================= #
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=auction_id,
            request_body=request_body,
            table_name=auctions_table_name,
            attributesTypeDict=AuctionsAttributesTypes,
            attributesEnum=AuctionsAttributes,
            dynamodb_client=dynamodb_client
        )
        # return handle_put_auction(auction_id=auction_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        # ========================= #
        # DELETE /db/auction/{auction_id}
        # ========================= #
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=auction_id,
            table_name=auctions_table_name,
            dynamodb_client=dynamodb_client
        )
        # return handle_delete_auction(auction_id=auction_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)
