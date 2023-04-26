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
from common_utils import respond, TESSError, put_item_to_dynamodb, get_item_from_dynamodb, delete_item_from_dynamodb, deserializer_dynamodb_data_to_json_format, get_path, HTTPMethods, guid, create_item, conver_josn_to_dynamodb_format, write_batch_items_to_dynamodb, delete_batch_items_from_dynamodb, validate_delete_data_payload, handle_delete_item_from_dynamodb_with_hash_key
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

        if 'market_id' not in event['pathParameters']:
            raise KeyError("market_id is missing")
        market_id = event['pathParameters']['market_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return respond(err=None, res="get list of auctions from resource id")
    elif http_method == HTTPMethods.POST.value:

        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return post_list_of_auctions_to_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=auctions_table_name
        )

    elif http_method == HTTPMethods.DELETE.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return delete_list_of_auctions_from_dynamodb(
            request_body=request_body, dynamodb_client=dynamodb_client, table_name=auctions_table_name
        )
    else:
        raise Exception("http method is not supported")


def post_list_of_auctions_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    try:
        if 'data' not in request_body:
            raise KeyError("data is missing")
        json_data = request_body['data']
        # convert json data to dynamodb format
        dynamodb_items, created_hash_key_values = conver_josn_to_dynamodb_format(
            hash_key=AuctionsAttributes.auction_id.name,
            items=json_data,
            attributesType=AuctionsAttributesTypes)
        # put data to dynamodb
        response = asyncio.run(write_batch_items_to_dynamodb(
            chunks=dynamodb_items, table_name=table_name, dynamodb_client=dynamodb_client))

        return respond(err=None, res=json.dumps(created_hash_key_values))
    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)


def delete_list_of_auctions_from_dynamodb(request_body: str, dynamodb_client, table_name: str):
    try:
        if 'data' not in request_body:
            raise KeyError("data is missing")
        delete_data_list = request_body['data']
        # validate data
        validate_delete_data_payload(
            data_list=delete_data_list, hash_key=AuctionsAttributes.auction_id.name)
        # delete data from dynamodb
        response = asyncio.run(delete_batch_items_from_dynamodb(
            chunks=delete_data_list, table_name=table_name, dynamodb_client=dynamodb_client))
        return respond(err=None, res="delete auctions success")
    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)
    # =================================================================================================
    # Agent /db/auction/{auction_id}
    # =================================================================================================


def handle_auction_route(event, context):
    http_method = event['httpMethod']
    if http_method == HTTPMethods.GET.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        return handle_get_auction_from_auction_id(
            auction_id=auction_id, dynamodb_client=dynamodb_client, table_name=auctions_table_name
        )
    elif http_method == HTTPMethods.POST.value:
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])
        return handle_post_auction(request_body=request_body, table_name=auctions_table_name, dynamodb_client=dynamodb_client)
    elif http_method == HTTPMethods.PUT.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        if 'body' not in event:
            raise KeyError("body is missing")
        request_body = json.loads(event['body'])

        return handle_put_auction(auction_id=auction_id, request_body=request_body)
    elif http_method == HTTPMethods.DELETE.value:
        if 'auction_id' not in event['pathParameters']:
            raise KeyError("auction_id is missing")
        auction_id = event['pathParameters']['auction_id']
        return handle_delete_auction(auction_id=auction_id)
    else:
        return respond(err=TESSError("http method is not supported"), res=None)

# ========================= #
# GET /db/auction/{auction_id}
# ========================= #


def handle_get_auction_from_auction_id(auction_id: str, dynamodb_client: boto3.client, table_name: str):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=auction_id,
                key=AuctionsAttributes.auction_id.name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            auction_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=AuctionsAttributesTypes)
            return respond(err=None, res=auction_data)
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# create a new auction
# POST /db/auction/{auction_id}
# ========================= #

def handle_post_auction(request_body: dict, table_name: str = None, dynamodb_client: boto3.client = None):

    try:
        auction_id = str(guid())
        # create new auciton
        item = create_item(
            primary_key_name=AuctionsAttributes.auction_id.name,
            primary_key_value=auction_id,
            request_body=request_body,
            attributeType=AuctionsAttributesTypes,
            attributes=AuctionsAttributes
        )
        # if not exist, put data in it
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        return respond(err=None, res="post data to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# update an auction
# PUT /db/auction/{auction_id}
# ========================= #


def handle_put_auction(auction_id: str, request_body: dict, table_name: str = auctions_table_name, dynamodb_client: boto3.client = dynamodb_client):
    try:
        # check if auction_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=auction_id,
                key=AuctionsAttributes.auction_id.name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"auction_id {auction_id} is not exist, please use post method to create a new"), res=None)
        else:
            # update item
            valid_at = int(time.time())
            item = create_item(
                primary_key_name=AuctionsAttributes.auction_id.name,
                primary_key_value=auction_id,
                request_body=request_body,
                attributeType=AuctionsAttributesTypes,
                attributes=AuctionsAttributes
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put data to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


# ========================= #
# delete an auction
# DELETE /db/auction/{auction_id}
# ========================= #


def handle_delete_auction(auction_id: str, table_name: str = auctions_table_name, dynamodb_client: boto3.client = dynamodb_client):
    try:
        # check if auction_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=auction_id,
                key=AuctionsAttributes.auction_id.name,
                table_name=auctions_table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=AuctionsAttributes.auction_id.name,
                id=auction_id,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))
