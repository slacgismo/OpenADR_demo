import boto3
import json
import logging
import datetime
import time
import os
import uuid
dynamodb = boto3.client('dynamodb')
# table_name = 'openadr-NHEC-dev-orders'
orders_timestream_table_name = os.environ["ORDERS_TIMESTEAM_TABLE_NAME"]
timestream_db_name = os.environ["TIMESTREAM_DB_NAME"]

MARKET_START_TIME = "2020-01-01T00:00:00Z"
MARKET_INTERVAL_IN_SECONDS = 20
"""
PUT /db/order/<order_id>
"""
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'device_id': "get device id"})
            }
        elif http_method == 'PUT':
            if 'device_id' not in event['pathParameters']:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Missing device_id'})
                }
            else:
                device_id = event['pathParameters']['device_id']
                order_id = str(guid())
                quantity = 1
                price = 1
                payload = {
                    'order_id': order_id,
                    'quantity': quantity,
                    'price': price
                }

                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(payload)
                }

            # order_id = event['pathParameters']['order_id']
            # request_body = json.loads(event['body'])
            # device_id = request_body.get('device_id', None)
            # if device_id is None:
            #     logger.error("No device_id")
            # resource_id = request_body.get('resource_id', None)
            # if resource_id is None:
            #     logger.error("No resource_id")
            # quantity = request_body.get('quantity', None)
            # if quantity is None:
            #     logger.error("No quantity")
            # flexible = request_body.get('flexible', 0)
            # state = request_body.get('state', None)
            # if state is None:
            #     logger.error("No state")
            # price = request_body.get('price', None)
            # if price is None:
            #     logger.error("price")
            # order_info = dict()
            # order_info['order_id'] = order_id
            # order_info['resource_id'] = resource_id
            # order_info['quantity'] = quantity
            # order_info['flexible'] = flexible
            # order_info['state'] = state
            # order_info['price'] = price
            # aution id  from device or generate here?
            # order_info['auction_id'] = "12321"
            # retrun current market end time. (same as next market start time)

            # market_start_timestamp = convert_datetime_to_timsestamp(
            #     time_str=MARKET_START_TIME)
            # # get the current time
            # current_time = int(time.time())
            # time_since_start = current_time - market_start_timestamp
            # time_to_next_start = MARKET_INTERVAL_IN_SECONDS - \
            #     (time_since_start % MARKET_INTERVAL_IN_SECONDS)
            # global_time_to_next_start = current_time + time_to_next_start
            order_id = str(guid())
            quantity = 1
            price = 1
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'order_id': order_id, "quantity": quantity, "price": price})
            }
            # put_order_info_into_dynamodb(
            #     order_info = order_info,
            #     table_name=table_name,
            #     dynamodb_client =dynamodb
            # )

        else:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Unsupported HTTP method {http_method}'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }


def current_market_start_timestamp(
    market_start_time: str,
    market_interval: int,
) -> int:
    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=market_start_time)
    current_time = int(time.time())
    time_since_start = current_time - market_start_timestamp
    time_to_next_start = (time_since_start % market_interval)
    if time_to_next_start == 0:
        return current_time
    else:
        # return previouse market start time
        return current_time + time_to_next_start - (market_interval)


def convert_datetime_to_timsestamp(time_str: str) -> int:
    time_obj = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    # convert datetime object to timestamp
    if not datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ'):
        raise Exception("time_str is not in the correct format")

    market_start_timestamp = int(time_obj.timestamp())
    return int(market_start_timestamp)


def put_order_info_into_dynamodb(order_info: dict, table_name: str, dynamodb_client) -> dict:
    try:
        dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'order_id': {'S': order_info['order_id']},
                'device_id': {'S': order_info['device_id']},
                'auction_id': {'S': order_info['auction_id']},
                'flexible': {'N': str(order_info['flexible'])},
                'state': {'N': str(order_info['state'])},
                'resource_id': {'S': order_info['resource_id']},
                'quantity': {'N': str(order_info['quantity'])},
                'price': {'N': str(order_info['price'])},
                'valid_at': {'N': str(order_info['valid_at'])}
            }
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': 'Order {} successfully added to table {}'.format(order_info['order_id'], table_name)})
        }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error adding order to table {}: {}'.format(table_name, str(e))
        }


def get_order_info_from_dynamodb(order_id: str, table_name: str, dynamodb_client):
    try:
        response = dynamodb_client.query(
            TableName=table_name,
            KeyConditionExpression='order_id = :val',
            ExpressionAttributeValues={
                ':val': {'S': order_id}
            }
        )

        if 'Items' in response:
            items = []
            for item in response['Items']:
                items.append({
                    'order_id': item['order_id']['S'],
                    'device_id': item['device_id']['S'],
                    'auction_id': item['auction_id']['S'],
                    'flexible': item['flexible']['N'],
                    'state': item['state']['N'],
                    'resource_id': item['resource_id']['S'],
                    'quantity': item['quantity']['N'],
                    'price': item['price']['N'],
                    'valid_at': item['valid_at']['N']
                })

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(items[0])
            }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'body': 'No orders found with device ID: {}'.format(order_id)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,

            'body': 'Error retrieving orders: {}'.format(str(e))
        }


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]
