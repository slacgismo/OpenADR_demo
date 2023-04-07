from enum import Enum
from .S3Service import S3Service

import os
from process_acitons.task_definition_generator import (
    create_and_export_task_definition,
    VTN_TASK_VARIANTS_ENUM,
    VEN_TASK_VARIANTS_ENUM,
)
from typing import List
from .TerraformExecution import TerraformExecution
import logging

from pathlib import Path


class Agent:
    def __init__(
        self,
        agent_id: str,
        resource_id: str,
        market_interval_in_second: str,
        devices: List,
        backend_s3_bucket_name: str,
        s3_bucket_name_of_task_definition_file: str,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
        backend_region: str,
        terraformExecutionObject: TerraformExecution = None,
        task_definition_file_name: str = None,
        backend_s3_state_key: str = None,
        s3_service: S3Service = None,
        market_start_time: str = None,
        local_timezone: str = None


    ):
        self.s3_service = s3_service
        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_second = market_interval_in_second
        self.devices = devices
        self.market_start_time = market_start_time
        self.local_timezone = local_timezone

        self.s3_bucket_name_of_task_definition_file = (
            s3_bucket_name_of_task_definition_file
        )
        self.DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = (
            DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME
        )
        self.backend_s3_bucket_name = backend_s3_bucket_name
        self.backend_region = backend_region
        self.terraformExecutionObject = terraformExecutionObject
        self.ecs_terraform_execution = terraformExecutionObject
        self.task_definition_file_name = task_definition_file_name
        self.backend_s3_state_key = backend_s3_state_key
        logging.info("create backend hcl file=====================")

    def create_ecs_service(
        self,
    ):
        print("start to create take definition file=====================")
        worker_path = Path(__file__).parent.parent
        templates_abs_path = os.path.join(worker_path, "terraform/templates")
        print(f"templates_abs_path: {templates_abs_path}")
        (
            created_task_definiton_name_file_path,
            vtn_id,
            vens_info,
        ) = create_and_export_task_definition(
            agent_id=self.agent_id,
            resource_id=self.resource_id,
            market_interval_in_second=self.market_interval_in_second,
            devices=self.devices,
            env="${environment}",
            METER_API_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/meter",
            DEVICES_API_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/device",
            DISPATCHES_API_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/dispatch",
            EMULATED_DEVICE_API_URL="https://l7xxtd4xh9.execute-api.us-east-2.amazonaws.com/dev/battery_api",
            ORDERS_API_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/order",
            # METER_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.METER_API_URL.value}}}",
            # DEVICES_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.DEVICES_API_URL.value}}}",
            # DISPATCHES_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.DISPATCHES_API_URL.value}}}",
            app_image_vtn="${app_image_vtn}",
            app_image_ven="${app_image_ven}",
            log_group_name="${cloudwatch_name}",
            aws_region="${aws_region}",
            # EMULATED_DEVICE_API_URL=f"{{${VEN_TASK_VARIANTS_ENUM.EMULATED_DEVICE_API_URL.value}}}",
            vtn_address="${vtn_address}",
            vtn_port="${vtn_port}",
            # ORDERS_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.ORDERS_API_URL.value}}}",
            file_name=self.task_definition_file_name,
            path=templates_abs_path,
            market_start_time=self.market_start_time,
            local_timezone=self.local_timezone,

        )
        print(
            "created_task_definiton_name_file_path",
            created_task_definiton_name_file_path,
        )
        # 2. create ecs service
        self.ecs_terraform_execution.terraform_init()

        # ecs_terraform.terraform_plan()
        self.ecs_terraform_execution.terraform_apply()
        logging.info("========================================")
        logging.info(f"ECS service created successfully: {self.agent_id}")
        logging.info("========================================")

        created_task_definiton_name_file_path = os.path.join(
            templates_abs_path, self.task_definition_file_name
        )
        self.s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{self.agent_id}/{self.task_definition_file_name}",
        )

        # remove local task definition file
        os.remove(created_task_definiton_name_file_path)
        return

    def update_ecs_service(self):
        # implementation of update method goes here
        backend_s3_service = S3Service(
            bucket_name=self.backend_s3_bucket_name,
        )

        is_file_exist = backend_s3_service.check_file_exists(
            file_name=self.backend_s3_state_key
        )
        if not is_file_exist:
            raise Exception(f"File {self.backend_s3_state_key} does not exist")

        # check if the agenet id is already in the dynamodb table
        worker_path = Path(__file__).parent.parent
        templates_abs_path = os.path.join(worker_path, "terraform/templates")
        print(f"templates_abs_path: {templates_abs_path}")
        (
            created_task_definiton_name_file_path,
            vtn_id,
            vens_info,
        ) = create_and_export_task_definition(
            agent_id=self.agent_id,
            resource_id=self.resource_id,
            market_interval_in_second=self.market_interval_in_second,
            devices=self.devices,
            env="${environment}",
            METER_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.METER_API_URL.value}}}",
            DEVICES_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.DEVICES_API_URL.value}}}",
            DISPATCHES_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.DISPATCHES_API_URL.value}}}",
            app_image_vtn="${app_image_vtn}",
            app_image_ven="${app_image_ven}",
            log_group_name="${cloudwatch_name}",
            aws_region="${aws_region}",
            EMULATED_DEVICE_API_URL=f"{{${VEN_TASK_VARIANTS_ENUM.EMULATED_DEVICE_API_URL.value}}}",
            vtn_address="${vtn_address}",
            vtn_port="${vtn_port}",
            ORDERS_API_URL=f"{{${VTN_TASK_VARIANTS_ENUM.ORDERS_API_URL.value}}}",
            file_name=self.task_definition_file_name,
            path=templates_abs_path,
        )

        self.ecs_terraform_execution.terraform_init()
        # ecs_terraform.terraform_plan()
        self.ecs_terraform_execution.terraform_apply()
        logging.info("========================================")
        logging.info(f"ECS service updated successfully: {self.agent_id}")
        logging.info("========================================")
        # s3_service = S3Service(
        #     bucket_name=self.s3_bucket_name_of_task_definition_file,
        # )
        created_task_definiton_name_file_path = os.path.join(
            "../terraform/templates", self.task_definition_file_name
        )
        # update task definition file in s3
        self.s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{self.agent_id}/{self.task_definition_file_name}",
        )
        # remove local task definition file
        os.remove(created_task_definiton_name_file_path)
        return

    def delete_ecs_service(self) -> str:
        is_file_exist = self.s3_service.check_file_exists(
            file_name=self.backend_s3_state_key
        )
        if not is_file_exist:
            raise Exception(f"File {self.backend_s3_state_key} does not exist")
        # download task definition file

        source = f"task_definitions/{self.agent_id}/{self.task_definition_file_name}"

        destination = f"./terraform/templates/{self.task_definition_file_name}"

        is_file_exist = self.s3_service.check_file_exists(file_name=source)
        s3_service = S3Service(
            bucket_name=self.s3_bucket_name_of_task_definition_file,
        )

        s3_service.download_file(source=source, destination=destination)

        self.ecs_terraform_execution.terraform_init()
        self.ecs_terraform_execution.terraform_destroy()

        logging.info("========================================")
        logging.info(f"ECS service deleted successfully:{self.agent_id}")
        logging.info("========================================")
        os.remove(destination)

        # update the agent record in the dynamodb table

        return
