import boto3
import subprocess
from .invoke_terraform import create_backend_hcl_file, create_terraform_auto_tfvars_file
import os
from typing import List


class ECSService:
    def __init__(self,
                 agent_id: str = None,
                 resource_id: str = None,
                 market_interval_in_second: str = None,
                 ecs_cluster_name: str = None
                 ):
        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_second = market_interval_in_second
        self.task_definition_file = None
        self.ecs_cluster_name = ecs_cluster_name
        self.client = boto3.client('ecs')

    def creagte_backend_hcl_file(self,
                                 path: str,
                                 backend_hcl_filename: str,
                                 backend_s3_bucket: str,
                                 backend_s3_key: str,
                                 backend_region: str,
                                 backend_dynamodb_table: str) -> bool:

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

    def list_ecs_services(self) -> List[str]:
        try:
            response = self.client.list_services(cluster=self.ecs_cluster_name)
            service_names = []
            for service_arn in response['serviceArns']:
                service_names.append(service_arn.split('/')[-1])

            return service_names
        except Exception as e:
            print(e)
