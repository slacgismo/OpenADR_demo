from classes.S3Service import S3Service
import pytest
from unittest.mock import MagicMock
from unittest.mock import ANY


@pytest.fixture
def s3_service():
    return S3Service(bucket_name='test-bucket')


def test_download_file(s3_service):
    s3_service.s3.download_file = MagicMock(return_value=None)
    source = 'test-source'
    destination = 'test-destination'
    s3_service.download_file(source, destination)
    s3_service.s3.download_file.assert_called_with(
        s3_service.bucket_name, source, destination)


def test_upload_file(s3_service):
    s3_service.s3.upload_file = MagicMock(return_value=None)
    source = 'test-source'
    destination = 'test-destination'
    s3_service.upload_file(source, destination)
    s3_service.s3.upload_file.assert_called_with(
        source, s3_service.bucket_name, destination)


def test_check_file_exists(s3_service):
    s3_service.client.head_object = MagicMock(return_value=None)
    file_name = 'test-file'
    assert s3_service.check_file_exists(file_name) is True
    s3_service.client.head_object.assert_called_with(
        Bucket=s3_service.bucket_name, Key=file_name)


def test_remove_file(s3_service):
    s3_service.client.delete_object = MagicMock(return_value=None)
    file_name = 'test-file'
    s3_service.remove_file(file_name)
    s3_service.client.delete_object.assert_called_with(
        Bucket=s3_service.bucket_name, Key=file_name)


def test_validate_s3_bucket(s3_service):
    sts_service = MagicMock()
    sts_service.get_account_id.return_value = 'test-account-id'
    s3_service.s3.put_object = MagicMock(return_value=None)
    s3_service.validate_s3_bucket(sts_service)
    s3_service.s3.put_object.assert_called_with(
        Bucket=s3_service.bucket_name,
        Key='access/test-account-id.json',
        Body=ANY,
    )
