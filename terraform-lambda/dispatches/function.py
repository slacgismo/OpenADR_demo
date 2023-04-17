import boto3
import json
import os
dynamodb = boto3.client('dynamodb')

# table_name = 'openadr-NHEC-dev-dispatches'
dispatches_table_name = os.environ["DISPATCHES_TABLE_NAME"]
# GET /dispatch/{order_id}


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            order_id = event['pathParameters']['order_id']
            return get_dispatch_info_from_dynamodb(
                order_id=order_id,
                table_name=dispatches_table_name,
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

        response = dynamodb_client.get_item(
            TableName=dispatches_table_name,
            Key={
                'order_id': {'S': order_id}
            }
        )

        if 'Item' in response:
            item = response['Item']

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'order_id': item['order_id']['S'],
                    'quantity': item['quantity']['N'],
                    'record_time': item['record_time']['N'],
                    'valid_at': item['valid_at']['N']
                })
            }

        # If no objects are found, return a failure response
        else:
            message = {"error": "No objects found with order ID: {}".format(order_id)
                       }
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(message)
            }

    # If an error occurs, return an error response
    except Exception as e:
        message = {"error": f"Error retrieving object: {e}"}
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(message)
        }
