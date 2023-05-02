import os
import boto3
import json
import time
import re
sqs = boto3.client('sqs')
devices_table_name = os.environ.get('DEVICES_TABLE_NAME', None)
settings_table_name = os.environ.get('SETTINGS_TABLE_NAME', None)

devices_settings_event_sqs = os.environ.get('DEVICES_SETTING_EVENT_SQS', None)

""""
{"Records": [{"eventID": "9e7c09e01be9768ff862312135f37745", "eventName": "REMOVE", "eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "us-east-2", "dynamodb": {"ApproximateCreationDateTime": 1683051336.0, "Keys": {"device_id": {"S": "12123213"}}, "OldImage": {"device_id": {"S": "12123213"}}, "SequenceNumber": "200000000000583744259", "SizeBytes": 34, "StreamViewType": "NEW_AND_OLD_IMAGES"}, "eventSourceARN": "arn:aws:dynamodb:us-east-2:041414866712:table/openadr-NHEC-STAGING-devices/stream/2023-05-02T17:29:20.256"}]}

"""


def handler(event, context):
    try:
        print(f"event {event}")
        # parse records
        if 'Records' not in event:
            raise ValueError("No records in event")

        for record in event["Records"]:
            print(f"record: {record}")
            if 'eventSourceARN' not in record:
                raise ValueError("No eventSourceARN in record")
            eventSourceARN = record['eventSourceARN']
            if 'table' not in eventSourceARN:
                raise ValueError("No table in eventSourceARN")
            table_name = re.search(
                r":table\/(.+)\/stream", eventSourceARN).group(1)

            print(f"table_name: {table_name}")
            if table_name == devices_table_name or table_name == settings_table_name:
                message_body = json.dumps(record)
                print(
                    f"Sending message to queue {devices_settings_event_sqs}: {message_body}")
                response = sqs.send_message(
                    QueueUrl=devices_settings_event_sqs, MessageBody=message_body)
                print(f"response {response}")
    except Exception as e:
        print(e)
        # print('Error sending message to SQS')
        raise e
