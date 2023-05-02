import os
import boto3
import json
import time
sqs = boto3.client('sqs')
# devices_event_sqs = os.environ["DEVICES_EVENT_SQS"]
devices_event_sqs = os.environ.get('DEVICES_EVENT_SQS', None)
settings_event_sqs = os.environ.get('SETTINGS_EVENT_SQS', None)

devices_table_name = os.environ.get('DEVICES_TABLE_NAME', None)
settings_table_name = os.environ.get('SETTINGS_TABLE_NAME', None)


def handler(event, context):
    try:
        # curr_time = time.time()
        for record in event["Records"]:

            print(f"record: {record}")
            # table_name = record["eventSourceARN"].split("/")[-1]
            # if table_name == devices_table_name:
            #     queue_url = devices_event_sqs
            # elif table_name == settings_table_name:
            #     queue_url = settings_event_sqs
            # else:
            #     raise ValueError("Unknown table name in eventSourceARN")

            # message_body = json.dumps(record)
            # print(f"Sending message to queue {queue_url}: {message_body}")
            # response = sqs.send_message(
            #     QueueUrl=queue_url, MessageBody=message_body)
    except Exception as e:
        print(e)
        # print('Error sending message to SQS')
        raise e

# def handler(event, context):
#     # Send message to SQS queue
#     try:
#         for record in event["Records"]:
#             message_body = json.dumps(record)
#             print("record: ", record)
#             response = sqs.send_message(
#                 QueueUrl=devices_event_sqs, MessageBody=message_body)
#     except Exception as e:
#         print(e)
#         print('Error sending message to SQS')
#         raise e
