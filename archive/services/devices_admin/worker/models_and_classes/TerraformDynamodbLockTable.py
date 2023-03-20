
import os
from .invoke_terraform import create_backend_hcl_file, create_terraform_auto_tfvars_file

import subprocess


class TerraformDynamodbLockTable:
    def __init__(self,
                 path: str,
                 backend_hcl_filename: str,

                 backend_s3_bucket: str,
                 backend_s3_key: str,
                 backend_region: str,
                 backend_dynamodb_table: str

                 ) -> None:

        self.path = path
        self.backend_hcl_filename = backend_hcl_filename
        self.backend_s3_bucket = backend_s3_bucket
        self.backend_s3_key = backend_s3_key
        self.backend_region = backend_region
        self.backend_dynamodb_table = backend_dynamodb_table

    def create(self,
               terraform_auto_tfvars_file_name: str,
               terraform_auto_tfvars_params: dict,
               ) -> None:
        print("create dynamodb lock table")
        # check backend hcl file exists
        backend_file_path = os.path.join(self.path, self.backend_hcl_filename)
        if not os.path.exists(backend_file_path):
            # crete backend hcl file
            create_backend_hcl_file(
                path=self.path,
                backend_hcl_filename=self.backend_hcl_filename,
                backend_s3_bucket=self.backend_s3_bucket,
                backend_s3_key=self.backend_s3_key,
                backend_region=self.backend_region,
                backend_dynamodb_table=self.backend_dynamodb_table
            )
            print("create backend hcl file")

        # create terraform auto tfvars file
        create_terraform_auto_tfvars_file(
            path=self.path,
            terraform_auto_tfvars_file_name=terraform_auto_tfvars_file_name,
            params=terraform_auto_tfvars_params
        )
        # invoke terraform t
        try:
            result = subprocess.run(
                ['docker-compose', 'run', '--rm', 'terraform', 'init', '-backend-config=backend.hcl', '-reconfigure'], cwd='./terraform_dynamodb')
            if result.returncode == 1:
                raise Exception(
                    "Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when terrafrom init dynamodb : {e}")
            # terraform validate
        try:
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'validate'], cwd='./terraform_dynamodb')
            if result.returncode == 1:
                raise Exception(
                    "Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error terrafrom validate dynamodb : {e}")
            # terraform validate
        try:
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'plan'], cwd='./terraform_dynamodb')
            if result.returncode == 1:
                raise Exception(
                    "Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when terrafrom plan dynamodb : {e}")
            # terraform apply auto-approve
        try:
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'apply', '--auto-approve'], cwd='./terraform_dynamodb')
            if result.returncode == 1:
                raise Exception(
                    "Subprocess returned error code 1, program stopped.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when terrafrom apply dynamodb : {e}")
        return
