
import boto3
from botocore.exceptions import ClientError
import time


class SQSService:
    def __init__(self, queue_url):
        self.queue_url = queue_url
        self.sqs = boto3.client('sqs')

    def receive_message(self, MaxNumberOfMessages: int = 1, WaitTimeSeconds: int = 20, VisibilityTimeout: int = 30):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=['All'],
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout,
                ReceiveRequestAttemptId=str(time.time())
            )

        except ClientError as e:
            print(
                f"Failed to receive message from SQS queue {self.queue_url}. Error: {e}")
            return None

        messages = response.get('Messages')
        if messages is not None:
            message = messages[0]
            return message

    def delete_message(self, receipt_handle):
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
        except ClientError as e:
            print(
                f"Failed to delete message from SQS queue {self.queue_url}. Error: {e}")

    def send_message(self, message_body):
        try:
            self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body
            )
        except ClientError as e:
            print(
                f"Failed to send message to SQS queue {self.queue_url}. Error: {e}")
