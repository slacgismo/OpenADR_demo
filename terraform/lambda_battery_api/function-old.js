import boto3
import json

dynamodb = boto3.client('dynamodb')
table_name = 'openadr-NHEC-dev-mock-battery'

get_battery_data = {
    "BackupBuffer": "10",
    "BatteryCharging": True,
    "BatteryDischarging": False,
    "Consumption_Avg": 0,
    "Consumption_W": 0,
    "Fac": 60,
    "FlowConsumptionBattery": True,
    "FlowConsumptionGrid": False,
    "FlowConsumptionProduction": False,
    "FlowGridBattery": True,
    "FlowProductionBattery": True,
    "FlowProductionGrid": True,
    "GridFeedIn_W": 196,
    "IsSystemInstalled": 1,
    "OperatingMode": "2",
    "Pac_total_W": -1800,
    "Production_W": 1792,
    "RSOC": 50,
    "RemainingCapacity_W": 5432,
    "SystemStatus": "OnGrid",
    "Timestamp": "2023-02-09 14:50:32",
    "USOC": 50,
    "Uac": 237,
    "Ubat": 54,
}


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            serial = event['pathParameters']['serial']
            return get_battery_info_from_dynamodb(
                serial=serial,
                table_name=table_name,
                dynamodb_client=dynamodb
            )

        elif http_method == 'POST':
            return {
                'statusCode': 200,
                'body': json.dumps({'serial': "post serial id"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error ': str(e)})
        }


def get_battery_info_from_dynamodb(serial: str, table_name: str, dynamodb_client):
    try:

        response = dynamodb_client.query(
            TableName=table_name,
            KeyConditionExpression='serial = :val',
            ExpressionAttributeValues={
                ':val': {'S': serial}
            }
        )
        if 'Items' in response:
            items = []
            if len(response['Items']) > 0 :
                for item in response['Items']:
                    items.append({
                        'serial': item['serial']['S'],
                        'token': item['token']['S']
                    })
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(get_battery_data)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': 'No objects found with serial: {}'.format(serial)
                }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'body': 'No objects found with serial: {}'.format(serial)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Error retrieving object: {}'.format(str(e))
        }