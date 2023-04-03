
import boto3
import json
import logging

dynamodb = boto3.client('dynamodb')
table_name = 'openadr-NHEC-dev-orders'

"""
PUT /db/order/<order_id>?<args...>
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
            if 'device_id' not in event['pathParameters']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Missing device_id'})
                }
            device_id = event['pathParameters']['device_id']
            query_params = event['queryStringParameters']
            if query_params is None:
                logger.error("No query params")

            resource_id = query_params.get('resource_id', None)
            if resource_id is None:
                logger.error("No resource_id")

            quantity = query_params.get('quantity', None)
            if quantity is None:
                logger.error("No quantity")

            flexible = query_params.get('flexible', 0)
            state = query_params.get('state', None)
            if state is None:
                logger.error("No state")

            record_time = query_params.get('record_time', None)
            if record_time is None:
                logger.error("No record_time")
            # simluate put data into db (dynamodb)
            # wait couple of seconds and get order_id back from dynamodb
            # return order id .
            return get_order_info_from_dynamodb(
                device_id=device_id,
                table_name=table_name,
                dynamodb_client=dynamodb
            )
            # return {
            #     'statusCode': 200,
            #     'body': json.dumps({
            #         'device_id': device_id,
            #         'resource_id': resource_id,
            #         'quantity': quantity,
            #         'flexible': flexible,
            #         'state': state,
            #         'record_time': record_time
            #     })
            # }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Unsupported HTTP method {http_method}'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_order_info_from_dynamodb(device_id: str, table_name: str, dynamodb_client):
    try:
        response = dynamodb_client.query(
            TableName=table_name,
            IndexName='device_id-index',  # Use the secondary index
            KeyConditionExpression='device_id = :val',
            ExpressionAttributeValues={
                ':val': {'S': device_id}
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
                    'valid_at': item['valid_at']['N'],
                    'record_time': item['record_time']['N']
                })

            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'body': 'No orders found with device ID: {}'.format(device_id)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error retrieving orders: {}'.format(str(e))
        }
