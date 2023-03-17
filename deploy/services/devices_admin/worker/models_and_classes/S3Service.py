import boto3
import os


class S3Service:
    def __init__(self, bucket_name: str):
        self.client = boto3.client('s3')
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def downlo_file(self, source, destination) -> None:
        try:
            response = self.s3.download_file(
                self.bucket_name, source, destination)
            print("Download file from s3 success")
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
