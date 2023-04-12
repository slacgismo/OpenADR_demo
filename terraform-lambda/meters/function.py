

import boto3
import json
import os
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('openadr-NHEC-dev-meters')
meters_table_name = os.environ["METERS_TABLE_NAME"]
# "PUT /meter/{device_id}/{meter_id}"


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'get meter': "get meter"})
            }
        elif http_method == 'PUT':
            device_id = event['pathParameters']['device_id']
            meter_id = event['pathParameters']['meter_id']
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'devce_id': device_id, "meter_id": meter_id})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
