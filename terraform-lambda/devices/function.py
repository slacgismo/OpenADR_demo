import boto3
import json

dynamodb = boto3.client('dynamodb')
# table = dynamodb.Table('openadr-NHEC-dev-devices')
table_name = 'openadr-NHEC-dev-devices'


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            device_id = event['pathParameters']['device_id']
            return get_device_info_from_dynamodb(
                device_id=device_id,
                table_name=table_name,
                dynamodb_client=dynamodb
            )

        elif http_method == 'POST':
            return {
                'statusCode': 200,
                'body': json.dumps({'devce_id': "post device id"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error ': str(e)})
        }


def get_device_info_from_dynamodb(device_id: str, table_name: str, dynamodb_client):
    try:

        response = dynamodb_client.query(
            TableName=table_name,
            KeyConditionExpression='device_id = :val',
            ExpressionAttributeValues={
                ':val': {'S': device_id}
            }
        )
        if 'Items' in response:
            items = []
            for item in response['Items']:
                items.append({
                    'device_id': item['device_id']['S'],
                    'agent_id': item['agent_id']['S'],
                    'device_type': item['device_type']['S'],
                    'valid_at': item['valid_at']['N']
                })

            return {
                'statusCode': 200,
                'body': json.dumps(items)
            }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'body': 'No objects found with device ID: {}'.format(device_id)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error retrieving object: {}'.format(str(e))
        }
