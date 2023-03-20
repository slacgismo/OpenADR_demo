from enum import Enum
from .S3Service import S3Service
from .DynamoDBService import DynamoDBService, DynamoDB_Key
import os
import time
from .helper.task_definition_generator import create_and_export_task_definition
from typing import List
from .TerraformExecution import TerraformExecution


class AgentState(Enum):

    ACTIVE = 'active'
    DELETED = 'deleted'
    DELETING = 'deleting'  # TODO: not implemented yet
    CREATING = 'creating'  # TODO: not implemented yet
    UPDATING = 'updating'  # TODO: not implemented yet

    FAILED_UPDATE = 'failed_update'  # TODO: not implemented yet
    FAILED_CREATE = 'failed_create'  # TODO: not implemented yet
    FAILED_DELETE = 'failed_delete'  # TODO: not implemented yet


class Agent:
    def __init__(self,
                 agent_id: str,
                 resource_id: str,
                 market_interval_in_second: str,
                 devices: List,
                 backend_s3_bucket_name: str,
                 s3_bucket_name_of_task_definition_file: str,
                 DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
                 backend_region: str
                 ):

        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_second = market_interval_in_second
        self.devices = devices

        self.s3_bucket_name_of_task_definition_file = s3_bucket_name_of_task_definition_file
        self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME
        self.backend_s3_bucket_name = backend_s3_bucket_name
        self.backend_region = backend_region

        print("create backend hcl file")

    def create_ecs_service(self,
                           backend_s3_state_key,
                           task_definition_file_name: str):

        created_task_definiton_name_file_path, vtn_id, vens_info = create_and_export_task_definition(
            agent_id=self.agent_id,
            resource_id=self.resource_id,
            market_interval_in_second=self.market_interval_in_second,
            devices=self.devices,
            env="${environment}",
            save_data_url="${SAVE_DATA_URL}",
            get_vens_url="${GET_VENS_URL}",
            participated_vens_url="${PARTICIPATED_VENS_URL}",
            app_image_vtn="${app_image_vtn}",
            app_image_ven="${app_image_ven}",
            log_group_name="${cloudwatch_name}",
            aws_region="${aws_region}",
            mock_devices_api_url="${MOCK_DEVICES_API_URL}",
            vtn_address="${vtn_address}",
            vtn_port="${vtn_port}",
            market_prices_url="${MARKET_PRICES_URL}",
            file_name=task_definition_file_name,
            path="./terraform/ecs/templates"

        )
        # create backend_hcl

        ecs_terraform = TerraformExecution(
            working_dir="./terraform/ecs",
            name_of_creation=f"ecs_service_{self.agent_id}",
            environment_variables={
                "task_definition_file": task_definition_file_name,
                "agent_id": self.agent_id
            },
            backend_s3_bucket_name=self.backend_s3_bucket_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            backend_region=self.backend_region
        )

        # 2. create ecs service
        ecs_terraform.terraform_init()
        # ecs_terraform.terraform_plan()
        ecs_terraform.terraform_apply()
        print("========================================")
        print("ECS service created successfully:", self.agent_id)
        print("========================================")
        # ecs_terraform.create()
        # 3. save s3 bucket
        s3_service = S3Service(
            bucket_name=self.s3_bucket_name_of_task_definition_file,
        )
        created_task_definiton_name_file_path = os.path.join(
            "./terraform/ecs/templates", task_definition_file_name
        )
        s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{self.agent_id}/{task_definition_file_name}"
        )

        # remove local task definition file
        os.remove(created_task_definiton_name_file_path)
        return

    def update_ecs_service(self,
                           task_definition_file_name: str,
                           backend_s3_state_key: str,
                           ):
        print("update ecs service")
        # implementation of update method goes here
        backend_s3_service = S3Service(
            bucket_name=self.backend_s3_bucket_name,
        )

        is_file_exist = backend_s3_service.check_file_exists(
            file_name=backend_s3_state_key)
        if not is_file_exist:
            raise Exception(
                f"File {backend_s3_state_key} does not exist")

        # check if the agenet id is already in the dynamodb table

        created_task_definiton_name_file_path, vtn_id, vens_info = create_and_export_task_definition(
            agent_id=self.agent_id,
            resource_id=self.resource_id,
            market_interval_in_second=self.market_interval_in_second,
            devices=self.devices,
            env="${environment}",
            save_data_url="${SAVE_DATA_URL}",
            get_vens_url="${GET_VENS_URL}",
            participated_vens_url="${PARTICIPATED_VENS_URL}",
            app_image_vtn="${app_image_vtn}",
            app_image_ven="${app_image_ven}",
            log_group_name="${cloudwatch_name}",
            aws_region="${aws_region}",
            mock_devices_api_url="${MOCK_DEVICES_API_URL}",
            vtn_address="${vtn_address}",
            vtn_port="${vtn_port}",
            market_prices_url="${MARKET_PRICES_URL}",
            file_name=task_definition_file_name,
            path="./terraform/ecs/templates"

        )

        # task_definition_file_name, backend_s3_state_key, backend_dynamodb_lock_name, destination = self._get_agent_info_from_dynamodb_and_s3()
        ecs_terraform = TerraformExecution(
            working_dir="./terraform/ecs",
            name_of_creation=f"ecs_service_{self.agent_id}",
            environment_variables={
                "task_definition_file": task_definition_file_name,
                "agent_id": self.agent_id
            },
            backend_s3_bucket_name=self.backend_s3_bucket_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            backend_region=self.backend_region
        )
        ecs_terraform.terraform_init()
        # ecs_terraform.terraform_plan()
        ecs_terraform.terraform_apply()
        print("========================================")
        print("ECS service updated successfully:", self.agent_id)
        print("========================================")
        s3_service = S3Service(
            bucket_name=self.s3_bucket_name_of_task_definition_file,
        )
        created_task_definiton_name_file_path = os.path.join(
            "./terraform/ecs/templates", task_definition_file_name
        )
        # update task definition file in s3
        s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{self.agent_id}/{task_definition_file_name}"
        )
        # remove local task definition file
        os.remove(created_task_definiton_name_file_path)
        return

    def delete_ecs_service(
        self,
        backend_s3_state_key,
        task_definition_file_name,
    ) -> str:
        # check if s3 state lock file exist
        backend_s3_service = S3Service(
            bucket_name=self.backend_s3_bucket_name,
        )

        is_file_exist = backend_s3_service.check_file_exists(
            file_name=backend_s3_state_key)
        if not is_file_exist:
            raise Exception(
                f"File {backend_s3_state_key} does not exist")
        # download task definition file

        source = f"task_definitions/{self.agent_id}/{task_definition_file_name}"

        destination = f"./terraform/ecs/templates/{task_definition_file_name}"
        is_file_exist = backend_s3_service.check_file_exists(
            file_name=source)
        s3_service = S3Service(
            bucket_name=self.s3_bucket_name_of_task_definition_file,
        )

        s3_service.download_file(
            source=source,
            destination=destination
        )

        ecs_terraform = TerraformExecution(
            working_dir="./terraform/ecs",
            name_of_creation=f"ecs_service_{self.agent_id}",
            environment_variables={
                "task_definition_file": task_definition_file_name,
                "agent_id": self.agent_id
            },
            backend_s3_bucket_name=self.backend_s3_bucket_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
            backend_region=self.backend_region
        )
        ecs_terraform.terraform_init()
        ecs_terraform.terraform_destroy()
        print("========================================")
        print("ECS service deleted successfully:", self.agent_id)
        print("========================================")
        os.remove(destination)

        # update the agent record in the dynamodb table

        return
