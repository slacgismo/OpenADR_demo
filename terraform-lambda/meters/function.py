

import boto3
import json
import os
import uuid
from enum import Enum
dynamodb = boto3.client('dynamodb')
# table = dynamodb.Table('openadr-NHEC-dev-meters')
meters_table_name = os.environ["METERS_TABLE_NAME"]
readings_timestream_table_name = os.environ["READINGS_TIMESTREAM_TABLE_NAME"]
timestream_db_name = os.environ["TIMESTREAM_DB_NAME"]
# "PUT /meter/{device_id}/{meter_id}"

timestream_write_client = boto3.client('timestream-write')


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
            # response = write_to_timestream(
            #     records=readings,
            #     meter_id=meter_id,
            #     device_id=device_id,
            #     resource_id=resource_id,
            #     device_brand=device_brand,
            #     status=status,
            #     timestamp=timestamp
            # )
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'message': 'success'})
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


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


async def write_to_timestream(records,
                              meter_id,
                              device_id,
                              resource_id,
                              device_brand,
                              status,
                              timestamp
                              ):
    dimensions = [
        {'Name': 'meter_id', 'Value': meter_id},
        {'Name': 'device_id', 'Value': device_id},
        {'Name': 'resource_id', 'Value': resource_id},
        {'Name': 'status', 'Value': resource_id},
        {'Name': 'device_brand', 'Value': device_brand}
    ]
    measures = []
    for key, value in records['readings'].items():
        if key in SonnenBatteryAttributeKey.__members__:
            measures.append({'Name': key, 'Value': str(value)})
    if len(measures) > 0:
        response = await timestream_write_client.write_records(DatabaseName=timestream_db_name,
                                                               TableName=readings_timestream_table_name,
                                                               Records=[{
                                                                   'Dimensions': dimensions,
                                                                   'MeasureName': 'readings',
                                                                   'MeasureValue': str(json.dumps(measures)),
                                                                   'Time': str(timestamp)
                                                               }])
        return response


class SonnenBatteryAttributeKey(Enum):
    BackupBuffer = 'BackupBuffer'
    BatteryCharging = 'BatteryCharging'
    BatteryDischarging = 'BatteryDischarging'
    # Consumption_Avg # exist but unused data
    Consumption_W = 'Consumption_W'
    Fac = 'Fac'
    FlowConsumptionBattery = 'FlowConsumptionBattery'
    FlowConsumptionGrid = 'FlowConsumptionGrid'
    FlowConsumptionProduction = 'FlowConsumptionProduction'
    FlowGridBattery = 'FlowGridBattery'
    FlowProductionBattery = 'FlowProductionBattery'
    FlowProductionGrid = 'FlowProductionGrid'
    GridFeedIn_W = 'GridFeedIn_W'
    # IsSystemInstalled  # exist but unused data
    OperatingMode = 'OperatingMode'
    Pac_total_W = 'Pac_total_W'
    Production_W = 'Production_W'
    # RSOC # exist but unused data
    RemainingCapacity_W = 'RemainingCapacity_W'
    SystemStatus = 'SystemStatus'
    USOC = 'USOC'
    Uac = 'Uac'
    Ubat = 'Ubat'
    Timestamp = 'Timestamp'
