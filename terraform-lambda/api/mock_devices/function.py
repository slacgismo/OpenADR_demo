import boto3
import json
from enum import Enum
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


class DeviceModels(Enum):
    SONNEN_BATTERY = 'sonnen_battery'
    EGAUGE = 'egauge'
    THEROMSTAT = 'thermostat'
    SOLAR = 'solar'
    WATER_HEATER = 'water_heater'


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            serial = event['pathParameters']['serial']
            query_params = event['queryStringParameters']
            if 'device_model' not in query_params:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error ': 'query_params is missing'})
                }
            device_model = query_params.get('device_model', None)
            if device_model is None:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error ': 'device_model is missing'})
                }
            if device_model.lower() == DeviceModels.SONNEN_BATTERY.value:
                # control mode
                enable_manual_mode = query_params.get(
                    'enable_manual_mode', None)
                if enable_manual_mode is not None:
                    payload = {
                        'enable_manual_mode': 1,
                        'status': 0
                    }
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(payload)
                    }
                manual_mode_control = query_params.get(
                    'manual_mode_control', None)
                if manual_mode_control is not None:
                    payload = {
                        'manual_mode_control': 1,
                        'ReturnCode': 0
                    }
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps(payload)
                    }

                # return battery data
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(get_battery_data)
                }
            else:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error ': f'device brand{device_model} not supported'})
                }
        elif http_method == 'PUT':
            serial = event['pathParameters']['serial']
            request_body = json.loads(event['body'])
            if 'device_model' not in request_body:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error ': 'device_model is missing'})
                }
            device_model = request_body['device_model']
            if device_model == DeviceModels.SONNEN_BATTERY.value:
                # control battery

                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(get_battery_data)
                }
            else:
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error ': f'device brand{device_model} not supported'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error ': str(e)})
        }
