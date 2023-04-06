import boto3
import json
import logging

dynamodb = boto3.client('dynamodb')
table_name = 'openadr-NHEC-dev-orders'

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
                'body': json.dumps({'device_id': "get device id"})
            }
        elif http_method == 'PUT':
            if 'order_id' not in event['pathParameters']:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Missing order_id'})
                }
            order_id = event['pathParameters']['order_id']
            request_body = json.loads(event['body'])
            device_id = request_body.get('device_id', None)
            if device_id is None:
                logger.error("No device_id")
            resource_id = request_body.get('resource_id', None)
            if resource_id is None:
                logger.error("No resource_id")
            quantity = request_body.get('quantity', None)
            if quantity is None:
                logger.error("No quantity")
            flexible = request_body.get('flexible', 0)
            state = request_body.get('state', None)
            if state is None:
                logger.error("No state")
            price = request_body.get('price', None)
            if price is None:
                logger.error("price")
            order_info = dict()
            order_info['order_id'] = order_id
            order_info['resource_id'] = resource_id
            order_info['quantity'] = quantity
            order_info['flexible'] = flexible
            order_info['state'] = state
            order_info['price'] = price
            order_info['auction_id'] = "12321"
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'order_id': order_id})
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
            'body': json.dumps({'error': str(e)})
        }


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
