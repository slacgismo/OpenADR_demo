import os
import boto3
import json
import time
from datetime import datetime
from enum import Enum
import uuid
from_event_queue_url = os.environ['SQS_QUEUE_URL']
to_trigger_queue_url = os.environ['SQS_TRIGGER_QUEUE_URL']
sqs = boto3.client('sqs')
'''
{'body': '{"eventID": "60edf1b1d52db87046e6ec8ca4c72f2f", "eventName": "MODIFY", "eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "us-east-2", "dynamodb": {"ApproximateCreationDateTime": 1681414497.0, "Keys": {"device_id": {"S": "37a6d01bf4009ae512d640ac594856d3"}}, "NewImage": {"agent_id": {"S": "2312"}, "device_id": {"S": "37a6d01bf4009ae512d640ac594856d3"}, "device_type": {"S": "ES"}, "valid_at": {"N": "1681414496"}}, "SequenceNumber": "7220700000000021559578469", "SizeBytes": 121, "StreamViewType": "NEW_IMAGE"}, "eventSourceARN": "arn:aws:dynamodb:us-east-2:041414866712:table/openadr-NHEC-dev-devices/stream/2023-04-12T06:46:05.602"}',
    'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-64385961-093b32c83faa42ef919c7c67;Parent=00e2cff84f1d3678;Sampled=0;Lineage=70eb5c3b:0', 'SentTimestamp': '1681414498103', 'SenderId': 'AROAQTJEEW4MMPJ2OY5Y3:openadr-NHEC-dev-lambda-dynamodb-event-trigger', 'ApproximateFirstReceiveTimestamp': '1681414498104'}, 'messageAttributes': {}, 'md5OfBody': '85db669ef954ebcc5c56dc6fb14942fe', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-2:041414866712:openadr-NHEC-dev-devices-sqs', 'awsRegion': 'us-east-2'}
'''


class EventName (Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


def handler(event, context):
    print(f"triggered by SQS :{event}")
    if event:
        batch_item_failures = []
        sqs_batch_response = {}

        for record in event["Records"]:
            try:

                # process message
                message_body = json.loads(record['body'])
                # Do something with the message body...
                if 'eventName' not in message_body:
                    raise Exception("eventName is missing from message body")

                eventName = message_body['eventName']
                handle_event(event_name=eventName, body=message_body,
                             to_trigger_queue_url=to_trigger_queue_url)
                # Delete the message
                response = sqs.delete_message(
                    QueueUrl=from_event_queue_url,
                    ReceiptHandle=record['receiptHandle']
                )
                print(f"Deleted message {record['messageId']}: {response}")

            except Exception as e:
                batch_item_failures.append(
                    {"itemIdentifier": record['messageId']})

        sqs_batch_response["batchItemFailures"] = batch_item_failures
        return sqs_batch_response


def handle_event(event_name: EventName, body: dict, to_trigger_queue_url: str = None):
    # parse new image
    if 'dynamodb'not in body or 'NewImage' not in body['dynamodb']:
        raise Exception("dynamodb or NewImage is missing from message body")
    new_image = body['dynamodb']['NewImage']

    if 'device_id' not in new_image or 'agent_id' not in new_image or 'device_type' not in new_image:
        raise Exception(
            "device_id, device_type or agent_id is missing from message body")
    device_id = new_image['device_id']['S']
    agent_id = new_image['agent_id']['S']
    device_type = new_image['device_type']['S']
    sq_message = create_sqs_message(
        device_id=device_id, agent_id=agent_id, eventName=event_name, device_type=device_type)
    response = send_message_to_sqs(
        message=sq_message, queue_url=to_trigger_queue_url)
    print(f"sqs response: {response}")


def create_sqs_message(device_id: str, agent_id: str, eventName: EventName, device_type: str):
    """
    {
    "eventName": "INSERT",
    "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
    "resource_id": "caff6719c24359a155a4d0d2f265a7",
    "market_interval_in_seconds": "300",
    "device_id": "807f8e4a37446e80c5756a74a3598d",
    "device_type": "ES",
    "meter_id": "6436a67e184d3694a15886215ae464"
    "device_settings": {
        "battery_token": "12321321qsd",
        "battery_sn": "66354",
        "device_brand": "SONNEN_BATTERY"
        "is_using_mock_device": true
        "flexible": "1",
    }

    }
    """
    # get meter_id from meter table
    meter_id = "6436a67e184d3694a15886215ae464"
    # get resource id from resource table
    resource_id = "caff6719c24359a155a4d0d2f265a7"
    # get market interval from market table
    market_interval_in_seconds = "60"
    # get device flexible  from setting table
    battery_token = "12321321qsd"
    battery_sn = "66354"
    device_brand = "SONNEN_BATTERY"
    is_using_mock_device = "true"
    flexible = "1"

    message = {
        "eventName": eventName,
        "agent_id": agent_id,
        "resource_id": resource_id,
        "market_interval_in_seconds": market_interval_in_seconds,
        "device_id": device_id,
        "device_type": device_type,
        "meter_id": meter_id,
        "device_settings": {
            "battery_token": battery_token,
            "battery_sn": battery_sn,
            "device_brand": device_brand,
            "is_using_mock_device": is_using_mock_device,
            "flexible": flexible
        }
    }
    print("Message created: ", message)
    return message


def send_message_to_sqs(message: dict, queue_url: str):
    sqs = boto3.client('sqs')
    print(f"Send to {queue_url}")
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageGroupId='AWS',
            MessageDeduplicationId=str(guid()),
            MessageBody=json.dumps(message)
        )
        print(f"Message sent to SQS: {response}")
    except Exception as e:
        print(f"Error sending message to SQS: {e}")
        raise e


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]
