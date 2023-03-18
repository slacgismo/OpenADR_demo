import boto3
import os


class S3Service:
    def __init__(self, bucket_name: str):

        self.client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def download_file(self, source, destination) -> None:
        try:
            response = self.s3.download_file(
                self.bucket_name, source, destination)
            print("Download file from s3 success", response)
            return None
        except Exception as e:
            raise Exception(f"Error when get object from s3: {e}")

    def upload_file(self, source, destination) -> None:
        try:
            response = self.s3.upload_file(
                source, self.bucket_name, destination)
            print("Save file to s3 success")
            return None
        except Exception as e:
            raise Exception(f"Error when put object to s3: {e}")

    # check if file exists in s3
    def check_file_exists(self, file_name: str) -> bool:
        try:
            response = self.client.head_object(
                Bucket=self.bucket_name, Key=file_name)
            print("File exists in s3")
            return True
        except Exception as e:
            print("File not exists in s3")
            return False

    # remove file from s3
    def remove_file(self, file_name: str) -> None:
        try:
            response = self.client.delete_object(
                Bucket=self.bucket_name, Key=file_name)
            print("File removed from s3")
            return None
        except Exception as e:
            raise Exception(f"Error when remove file from s3: {e}")
    # list all the objects in s3 bucket on a given path
