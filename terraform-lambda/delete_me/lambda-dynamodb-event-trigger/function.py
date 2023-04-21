import os
import boto3
import json
sqs = boto3.client('sqs')
queue_url = os.environ["SQS_QUEUE_URL"]


def handler(event, context):
    # Send message to SQS queue
    try:
        for record in event["Records"]:
            message_body = json.dumps(record)
            print("record: ", record)
            response = sqs.send_message(
                QueueUrl=queue_url, MessageBody=message_body)
    except Exception as e:
        print(e)
        print('Error sending message to SQS')
        raise e
