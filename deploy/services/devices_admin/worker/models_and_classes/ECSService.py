import boto3
import subprocess
from .invoke_terraform import create_backend_hcl_file, create_terraform_auto_tfvars_file
import os


class ECSService:
    def __init__(self,
                 agent_id,
                 resource_id,
                 market_interval_in_second

                 ):
        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_second = market_interval_in_second
        self.task_definition_file = None
        self.client = boto3.client('ecs')

    def creagte_backend_hcl_file(self,
                                 path: str,
                                 backend_hcl_filename: str,
                                 backend_s3_bucket: str,
                                 backend_s3_key: str,
                                 backend_region: str,
                                 backend_dynamodb_table: str) -> bool:
        # backend_file_path = os.path.join(path, backend_hcl_filename)
        # if not os.path.exists(backend_file_path):
        # crete backend hcl file
        # alawys overwrite the backend hcl file
        create_backend_hcl_file(
            path=path,
            backend_hcl_filename=backend_hcl_filename,
            backend_s3_bucket=backend_s3_bucket,
            backend_s3_key=backend_s3_key,
            backend_region=backend_region,
            backend_dynamodb_table=backend_dynamodb_table
        )
        print("create backend hcl file")
        return True

    def create_terraform_auto_tfvars_file(self,
                                          path: str,
                                          terraform_auto_tfvars_file_name: str,
                                          params: dict) -> bool:
        create_terraform_auto_tfvars_file(
            path=path,
            terraform_auto_tfvars_file_name=terraform_auto_tfvars_file_name,
            params=params
        )
        print("create terraform auto tfvars file")
        return True

    def create(self, is_creating_empty_ecs_service: bool):

        print("create_ecs_service")
        if is_creating_empty_ecs_service is True:
            print("Create empty ecs services")
        else:

            # create the dynamodb table
            try:
                result = subprocess.run(
                    ['docker-compose', 'run', '--rm', 'terraform', 'init', '-backend-config=backend.hcl'], cwd='./terraform_ecs')
                # terraform validate
                if result.returncode != 0:
                    raise Exception("Error when creating ecs service")
                result = subprocess.run(['docker-compose', 'run', '--rm',
                                         'terraform', 'validate'], cwd='./terraform_ecs')
                if result.returncode != 0:
                    raise Exception("Error when creating ecs service")
                # terraform validate
                result = subprocess.run(['docker-compose', 'run', '--rm',
                                         'terraform', 'plan'], cwd='./terraform_ecs')
                if result.returncode != 0:
                    raise Exception("Error when creating ecs service")
                # terraform apply auto-approve
                result = subprocess.run(['docker-compose', 'run', '--rm',
                                         'terraform', 'apply', '--auto-approve'], cwd='./terraform_ecs')
                if result.returncode != 0:
                    raise Exception("Error when creating ecs service")
            except subprocess.CalledProcessError as e:
                raise Exception(f"Error when creating ecs service: {e}")
            # create the ecs service

        return

    def delete(self):
        print("delete ecs service")
        try:
            result = subprocess.run(
                ['docker-compose', 'run', '--rm', 'terraform', 'init', '-backend-config=backend.hcl'], cwd='./terraform_ecs')
            # terraform validate
            if result.returncode != 0:
                raise Exception("Error when creating ecs service")
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'validate'], cwd='./terraform_ecs')
            if result.returncode != 0:
                raise Exception("Error when validate ecs service")
            # terraform validate
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'plan'], cwd='./terraform_ecs')
            if result.returncode != 0:
                raise Exception("Error when plan ecs service")
            # terraform apply auto-approve
            result = subprocess.run(['docker-compose', 'run', '--rm',
                                     'terraform', 'destroy', '--auto-approve'], cwd='./terraform_ecs')
            if result.returncode != 0:
                raise Exception("Error when destroy ecs service")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error when creating ecs service: {e}")
        return

    def update(self):
        print("update ecs service")
        return
