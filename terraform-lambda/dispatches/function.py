import boto3
import json

dynamodb = boto3.client('dynamodb')

table_name = 'openadr-NHEC-dev-dispatches'

# GET /dispatch/{order_id}


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            order_id = event['pathParameters']['order_id']
            return get_dispatch_info_from_dynamodb(
                order_id=order_id,
                table_name=table_name,
                dynamodb_client=dynamodb
            )

        elif http_method == 'POST':
            return {
                'statusCode': 200,
                'body': json.dumps({'order': "dispatch post order id"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error ': str(e)})
        }


def get_dispatch_info_from_dynamodb(order_id: str, table_name: str, dynamodb_client):
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
                    'quantity': item['quantity']['N'],
                    'record_time': item['record_time']['N'],
                    'valid_at': item['valid_at']['N']
                })

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(items)
            }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'body': 'No objects found with order ID: {}'.format(order_id)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error retrieving object: {}'.format(str(e))
        }
