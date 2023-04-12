import asyncio
import boto3
import json
import time
import os
dynamodb = boto3.client('dynamodb')
# table = dynamodb.Table('openadr-NHEC-dev-devices')
# table_name = 'openadr-NHEC-dev-devices'
devices_table_name = os.environ["DEVICES_TABLE_NAME"]


def handler(event, context):
    try:
        http_method = event['httpMethod']
        if http_method == 'GET':
            device_id = event['pathParameters']['device_id']
            return asyncio.run(get_device_info_from_dynamodb(
                device_id=device_id,
                table_name=devices_table_name,
                dynamodb_client=dynamodb
            ))

        elif http_method == 'PUT':
            device_id = event['pathParameters']['device_id']
            request_body = json.loads(event['body'])
            device_type = request_body.get('device_type', None)
            agent_id = request_body.get('agent_id', None)
            valid_at = int(time.time())
            # save data to dynamodb
            return asyncio.run(put_device_info_to_dynamodb(
                device_id=device_id,
                device_type=device_type,
                agent_id=agent_id,
                valid_at=valid_at,
                table_name=devices_table_name,
                dynamodb_client=dynamodb
            ))

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error ': str(e)})
        }


async def put_device_info_to_dynamodb(device_id: str, device_type: str, agent_id: str, valid_at: int, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(dynamodb_client.put_item,
                                           TableName=table_name,
                                           Item={
                                               'device_id': {'S': device_id},
                                               'device_type': {'S': device_type},
                                               'agent_id': {'S': agent_id},
                                               'valid_at': {'N': str(valid_at)}
                                           }
                                           )
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error ': str(e)})
        }


async def get_device_info_from_dynamodb(device_id: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(dynamodb_client.query,
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
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(items)
            }

        # If no objects are found, return a failure response
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/text'},
                'body': 'No objects found with device ID: {}'.format(device_id)
            }

    # If an error occurs, return an error response
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/text'},
            'body': json.dumps({"error": str(e)})
        }
