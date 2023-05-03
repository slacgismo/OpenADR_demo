import boto3
from . import STSService
import time
import json


class S3Service:
    def __init__(self, bucket_name: str):
        self.client = boto3.client("s3")
        self.bucket_name = bucket_name
        self.s3 = boto3.client("s3")

    def download_file(self, source, destination) -> None:
        try:
            response = self.s3.download_file(
                self.bucket_name, source, destination)
            print(f"Download {destination} from s3 success", response)
            return None
        except Exception as e:
            raise Exception(f"Error when get object from s3: {e}")

    def upload_file(self, source, destination) -> None:
        try:
            response = self.s3.upload_file(
                source, self.bucket_name, destination)
            print(f"Save {destination} to s3 success")
            return None
        except Exception as e:
            raise Exception(f"Error when put {destination} to s3: {e}")

    # check if file exists in s3
    def check_file_exists(self, file_name: str) -> bool:
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name, Key=file_name)
            print(f"{file_name} exists in s3 {self.bucket_name}")
            return True
        except Exception as e:
            print(f"{file_name} not exists in s3 {e}")
            return False

    # remove file from s3
    def remove_file(self, file_name: str) -> None:
        try:
            response = self.client.delete_object(
                Bucket=self.bucket_name, Key=file_name)
            print("File removed from s3")
            return None
        except Exception as e:
            raise Exception(f"Error when remove {file_name} from s3: {e}")

    # list all the objects in s3 bucket on a given path

    def validate_s3_bucket(self, sts_service: STSService) -> None:
        try:
            account_id = sts_service.get_account_id()
            current_time = str(int(time.time()))
            data = {"account_id": account_id, "time": current_time}
            # save data to s3
            response = self.s3.put_object(
                Bucket=self.bucket_name,
                Key=f"access/{account_id}.json",
                Body=json.dumps(data),
            )

            print("Validate s3 bucket write access success")

            return None
        except Exception as e:
            raise Exception(f"Error when validate s3 bucket: {e}")
