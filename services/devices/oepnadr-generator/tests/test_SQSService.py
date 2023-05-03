import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from classes.SQSService import SQSService


@pytest.fixture
def sqs_service():
    # Replace "queue-url" with the actual URL of your test SQS queue
    return SQSService(queue_url="queue-url")


def test_receive_message_success(sqs_service):
    # Create a mock SQS message
    message = {
        "Attributes": {"MessageGroupId": "group-1"},
        "ReceiptHandle": "receipt-handle-1",
        "MessageId": "message-id-1",
        "Body": "Test message body",
    }
    # Create a mock SQS response
    response = {"Messages": [message]}

    # Create a mock SQS client that returns the mock response
    sqs_client_mock = MagicMock()
    sqs_client_mock.receive_message.return_value = response
    sqs_service.sqs = sqs_client_mock

    # Call the method under test
    result = sqs_service.receive_message(group_id="group-1")

    # Check that the correct message was returned
    assert result == message


def test_receive_message_no_messages(sqs_service):
    # Create a mock SQS response with no messages
    response = {"Messages": None}

    # Create a mock SQS client that returns the mock response
    sqs_client_mock = MagicMock()
    sqs_client_mock.receive_message.return_value = response
    sqs_service.sqs = sqs_client_mock

    # Call the method under test
    result = sqs_service.receive_message(group_id="group-1")

    # Check that None was returned
    assert result is None


def test_receive_message_wrong_group_id(sqs_service):
    # Create a mock SQS message with a different group ID
    message = {
        "Attributes": {"MessageGroupId": "group-2"},
        "ReceiptHandle": "receipt-handle-1",
        "MessageId": "message-id-1",
        "Body": "Test message body",
    }
    # Create a mock SQS response with the message
    response = {"Messages": [message]}

    # Create a mock SQS client that returns the mock response
    sqs_client_mock = MagicMock()
    sqs_client_mock.receive_message.return_value = response
    sqs_service.sqs = sqs_client_mock

    # Call the method under test
    result = sqs_service.receive_message(group_id="group-1")

    # Check that None was returned
    assert result is None


def test_delete_message(sqs_service):
    sqs_service.sqs.delete_message = MagicMock()
    sqs_service.delete_message(receipt_handle="123")
    sqs_service.sqs.delete_message.assert_called_with(
        QueueUrl="queue-url", ReceiptHandle="123")


def test_purge_message(sqs_service):
    sqs_service.sqs.purge_queue = MagicMock()
    sqs_service.purge_message()
    sqs_service.sqs.purge_queue.assert_called_with(QueueUrl="queue-url")
