import boto3
import subprocess
from process_acitons.create_backend_hcl_file import (
    create_backend_hcl_file,
)
from process_acitons.create_terraform_auto_tfvars_file import create_terraform_auto_tfvars_file
import os
from typing import List


class ECSService:
    def __init__(
        self,
        agent_id: str = None,
        resource_id: str = None,
        market_interval_in_seconds: str = None,
        ecs_cluster_name: str = None,
    ):
        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_seconds = market_interval_in_seconds
        self.task_definition_file = None
        self.ecs_cluster_name = ecs_cluster_name
        self.client = boto3.client("ecs")

    def list_ecs_services(self) -> List[str]:
        try:
            response = self.client.list_services(cluster=self.ecs_cluster_name)
            service_names = []
            for service_arn in response["serviceArns"]:
                service_names.append(service_arn.split("/")[-1])

            return service_names
        except Exception as e:
            print(e)
