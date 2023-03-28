import boto3
from botocore.exceptions import ClientError
import time
import logging
from process_acitons.guid import guid


class SQSService:
    def __init__(
        self,
        queue_url,
    ):
        self.queue_url = queue_url

        self.sqs = boto3.client("sqs")

    def receive_message(
        self,
        MaxNumberOfMessages: int = 1,
        WaitTimeSeconds: int = 20,
        VisibilityTimeout: int = 30,
        group_id: str = None,
    ):
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=["All"],
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=MaxNumberOfMessages,
                WaitTimeSeconds=WaitTimeSeconds,
                VisibilityTimeout=VisibilityTimeout,
                ReceiveRequestAttemptId=str(time.time()),
            )
            # messages = response.get('Messages')
            messages = response.get("Messages")
            if messages is None:
                return None

            for message in messages:
                Attributes = message.get("Attributes")
                MessageGroupId = Attributes.get("MessageGroupId")
                ReceiptHandle = message.get("ReceiptHandle")

                if MessageGroupId == group_id:
                    # if the message is for this group id then process it
                    # delete the message from the queue
                    self.delete_message(receipt_handle=ReceiptHandle)
                    return message
                else:
                    # not this group id so ignore it
                    logging.info(f"Ignore group id {MessageGroupId}")
                    return None
        except ClientError as e:
            raise (
                f"Failed to receive message from SQS queue {self.queue_url}. Error: {e}"
            )

    def delete_message(self, receipt_handle):
        try:
            logging.info(f"delete_message")
            self.sqs.delete_message(
                QueueUrl=self.queue_url, ReceiptHandle=receipt_handle
            )
        except ClientError as e:
            raise (
                f"Failed to delete message from SQS queue {self.queue_url}. Error: {e}"
            )

    def send_message(
        self, message_body=None, message_attributes=None, message_group_id=None
    ):
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageAttributes=message_attributes,
                MessageGroupId=message_group_id,
                MessageDeduplicationId=str(guid),
                MessageBody=message_body,
            )

        except ClientError as e:
            raise (
                f"Failed to send message to SQS queue {self.queue_url}. Error: {e}")

    def purge_message(self):
        try:
            self.sqs.purge_queue(QueueUrl=self.queue_url)
        except ClientError as e:
            raise (
                f"Failed to purge message from SQS queue {self.queue_url}. Error: {e}"
            )

    def send_message_batch(self, sqs_messages):
        try:
            # for batch in [sqs_messages[i:i+10] for i in range(0, len(sqs_messages), 10)]:
            response = self.sqs.send_message_batch(
                QueueUrl=self.queue_url, Entries=sqs_messages
            )
            return response
        except ClientError as e:
            raise (
                f"Failed to send message to SQS queue {self.queue_url}. Error: {e}")
