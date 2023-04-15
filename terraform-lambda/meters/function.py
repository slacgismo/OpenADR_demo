

import boto3
import json
import os
import uuid
from enum import Enum
dynamodb = boto3.client('dynamodb')
# table = dynamodb.Table('openadr-NHEC-dev-meters')
meters_table_name = os.environ["METERS_TABLE_NAME"]
readings_table_name = os.environ["READINGS_TABLE_NAME"]
# "PUT /meter/{device_id}/{meter_id}"


class MetersDataKeys(Enum):
    RESOURCE_ID = "resource_id"
    READINGS = "readings"
    DEVICE_BRAND = "device_brand"
    STATUS = "status"
    TIMESTAMP = "timestamp"


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            meter_id = event['pathParameters']['meter_id']
            device_id = event['pathParameters']['device_id']
            request_body = json.loads(event['body'])
            # parse the request body
            resource_id = request_body[MetersDataKeys.RESOURCE_ID.value]
            readings = request_body[MetersDataKeys.READINGS.value]
            device_brand = request_body[MetersDataKeys.DEVICE_BRAND.value]
            status = request_body[MetersDataKeys.STATUS.value]
            timestamp = request_body[MetersDataKeys.TIMESTAMP.value]
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'readings': readings})
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


# def save_to_readings_table(device_id, meter_id, readings):
#     # save readings to readings table
#     timestream_client = boto3.client('timestream-write')
#     reading_id = str(uuid.uuid4())
#     for reading in readings:
#         table.put_item(
#             Item={
#                 'device_id': device_id,
#                 'meter_id': meter_id,
#                 'reading': reading
#             }
#         )


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]
