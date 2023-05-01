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
from common_utils import respond, TESSError, HTTPMethods, guid, handle_delete_item_from_dynamodb_with_hash_key, handle_put_item_to_dynamodb_with_hash_key, handle_create_item_to_dynamodb, handle_get_item_from_dynamodb_with_hash_key, create_items_to_dynamodb, delete_items_from_dynamodb, handle_query_items_from_dynamodb, handle_scan_items_from_dynamodb, match_path
dynamodb_client = boto3.client('dynamodb')

auctions_table_name = os.environ.get("AUCTIONS_TABLE_NAME", None)
auctions_table_market_id_valid_at_gsi = os.environ.get(
    "AUCTIONS_TABLE_MARKET_ID_VALID_AT_GSI", None)

environment_variables_list = []
environment_variables_list.append(auctions_table_name)
environment_variables_list.append(auctions_table_market_id_valid_at_gsi)


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
    AuctionsAttributes.auction_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.market_id.value: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AuctionsAttributes.clearing_time.value: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AuctionsAttributes.expected_price.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.expected_stdev.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.reference_price.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.price.value: {
        'dynamodb_type': 'N',
        'return_type': 'float'
    },
    AuctionsAttributes.quantity.value: {
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


class AuctionsRouteKeys(Enum):
    auctions = "auctions"
    auction = "auction"
    auctions_query = "auctions/query"
    auctions_scan = "auctions/scan"

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

        if match_path(path=path, route_key=AuctionsRouteKeys.auctions.value):
            return handle_auctions_route(event=event, context=context)
        elif match_path(path=path, route_key=AuctionsRouteKeys.auction.value):
            return handle_auction_route(event=event, context=context)
        elif match_path(path=path, route_key=AuctionsRouteKeys.auctions_query.value):
            return handle_auctions_query_route(event=event, context=context)
        elif match_path(path=path, route_key=AuctionsRouteKeys.auctions_scan.value):
            return handle_auctions_scan_route(event=event, context=context)
    except Exception as e:
        return respond(err=TESSError(str(e)))

    # =================================================================================================
    # Auctions /db/auctions/{get_items_action}
    # =================================================================================================


def handle_auctions_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return create_items_to_dynamodb(
            request_body=request_body,
            dynamodb_client=dynamodb_client,
            table_name=auctions_table_name,
            hash_key_name=AuctionsAttributes.auction_id.name,
            attributesTypeDict=AuctionsAttributesTypes
        )
    elif http_method == HTTPMethods.DELETE.value:
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

    # =================================================================================================
    # Agent /db/auction/{auction_id}
    # =================================================================================================


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
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # create a new auction
        # POST /db/auction/{auction_id}
        # ========================= #
        return handle_create_item_to_dynamodb(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=str(guid()),
            request_body=request_body,
            table_name=auctions_table_name,
            attributeTypeDice=AuctionsAttributesTypes,
            attributesEnum=AuctionsAttributes,
            dynamodb_client=dynamodb_client

        )

    elif http_method == HTTPMethods.PUT.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        # ========================= #
        # update an auction
        # PUT /db/auction/{auction_id}
        # ========================= #

        return handle_put_item_to_dynamodb_with_hash_key(
            hash_key_name=AuctionsAttributes.auction_id.name,
            hash_key_value=auction_id,
            request_body=request_body,
            table_name=auctions_table_name,
            attributesTypeDict=AuctionsAttributesTypes,
            attributesEnum=AuctionsAttributes,
            dynamodb_client=dynamodb_client
        )
    elif http_method == HTTPMethods.DELETE.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        # ========================= #
        # delete an auction
        # DELETE /db/auction/{auction_id}
        # ========================= #
        return handle_delete_item_from_dynamodb_with_hash_key(
            hash_key_name=AuctionsAttributes.auction_id.name, hash_key_value=auction_id, table_name=auctions_table_name, dynamodb_client=dynamodb_client
        )
    else:
        return respond(err=TESSError("http method is not supported"))

# ========================= #
# query an auction
# GET /db/auction/query
# ========================= #


def handle_auctions_query_route(event, context):

    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_query_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=auctions_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=AuctionsAttributesTypes,
            environment_variables_list=environment_variables_list,

        )
    else:
        raise Exception(f"unsupported http method {http_method}")

# ========================= #
# scan an auction
# GET /db/auction/scans
# ========================= #


def handle_auctions_scan_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        # get query string parameters from event
        query_string_parameters = event['queryStringParameters']
        if query_string_parameters is None:
            raise KeyError("query string parameters are missing")
        return handle_scan_items_from_dynamodb(
            query_string_parameters=query_string_parameters,
            table_name=auctions_table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=AuctionsAttributesTypes,
        )
    else:
        raise Exception(f"unsupported http method {http_method}")
