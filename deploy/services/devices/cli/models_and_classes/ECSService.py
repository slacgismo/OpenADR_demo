import boto3
import subprocess

import os
from typing import List


class ECSService:
    def __init__(self,
                 ecs_cluster_name: str = None
                 ):

        self.ecs_cluster_name = ecs_cluster_name
        self.client = boto3.client('ecs')

    def list_ecs_services(self) -> List[str]:
        try:
            response = self.client.list_services(cluster=self.ecs_cluster_name)

            service_names = []
            for service_arn in response['serviceArns']:
                service_names.append(service_arn.split('/')[-1])

            return service_names

        except Exception as e:
            print(e)
