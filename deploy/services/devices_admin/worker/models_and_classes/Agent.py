from enum import Enum
from .S3Service import S3Service
from .DynamoDBService import DynamoDBService, DynamoDB_Key
import os
import time
from .helper.task_definition_generator import create_and_export_task_definition
from typing import List
from .TerraformExecution import TerraformExecution


class AgentState(Enum):
    # CREATE = 'create'
    ACTIVE = 'active'
    DELETED = 'deleted'


class Agent:
    def __init__(self,
                 agent_id: str,
                 resource_id: str,
                 market_interval_in_second: str,
                 devices: List,
                 backend_s3_bucket_name: str,
                 s3_bucket_name_of_task_definition_file: str,
                 dynamodb_agents_table_name: str,
                 backend_region: str
                 ):

        self.agent_id = agent_id
        self.resource_id = resource_id
        self.market_interval_in_second = market_interval_in_second
        self.devices = devices

        self.s3_bucket_name_of_task_definition_file = s3_bucket_name_of_task_definition_file
        self.dynamodb_agents_table_name = dynamodb_agents_table_name
        self.backend_s3_bucket_name = backend_s3_bucket_name
        self.backend_region = backend_region

        print("create backend hcl file")

    def create_ecs_service(self,
                           backend_s3_state_key,
                           backend_dynamodb_lock_name,
                           task_definition_file_name: str):

        backend_dynanmodb_service = DynamoDBService(
            table_name=backend_dynamodb_lock_name)
        is_table_exist = backend_dynanmodb_service.check_if_table_exist()
        if not is_table_exist:
            raise Exception(
                f"Table {backend_dynamodb_lock_name} does not exist")
        backend_s3_service = S3Service(
            bucket_name=self.backend_s3_bucket_name,
        )

        is_file_exist = backend_s3_service.check_file_exists(
            file_name=backend_s3_state_key)
        if is_file_exist:
            raise Exception(
                f"File {backend_s3_state_key} does exist, this use update instead of create")
        # 1. create ecs service
        # agents_dynanmodb_service = DynamoDBService(
        #     table_name=self.dynamodb_agents_table_name)
        # if agents_dynanmodb_service.check_if_agent_id_exist(agent_id=self.agent_id):
        #     raise Exception(
        #         f"Agent {self.agent_id} exist, please use another agent id")
        # check if the agenet id is already in the dynamodb table
        # result = agents_dynanmodb_service.get_item(agent_id=self.agent_id)
        # if len(result) > 0:
        #     raise Exception(f"Agent {self.agent_id} already exists")
        # # if yes, raise an error
        # # if no, create a new record in the dynamodb table
        # return
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
        # crea backend_hcl

        ecs_terraform = TerraformExecution(
            working_dir="./terraform/ecs",
            name_of_creation=f"ecs_service_{self.agent_id}",
            environment_variables={
                "task_definition_file": task_definition_file_name,
                "agent_id": self.agent_id
            },
            backend_s3_bucket_name=self.backend_s3_bucket_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=backend_dynamodb_lock_name,
            backend_region=self.backend_region
        )
        # 2. create ecs service
        ecs_terraform.terraform_init()
        ecs_terraform.terraform_plan()
        ecs_terraform.terraform_apply()
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
        # 4. save dynamodb table

        # item = {
        #     DynamoDB_Key.AGENT_ID.value: self.agent_id,
        #     DynamoDB_Key.RESOURCE_ID.value: self.resource_id,
        #     DynamoDB_Key.VTN_ID.value: vtn_id,
        #     DynamoDB_Key.VENS.value: vens_info,
        #     DynamoDB_Key.VALID_AT.value: str(int(time.time())),

        #     DynamoDB_Key.BACKEND_S3_STATE_KEY.value: backend_s3_state_key,
        #     DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value: backend_dynamodb_lock_name,
        #     DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value: task_definition_file_name,
        #     DynamoDB_Key.STATE.value: AgentState.ACTIVE.value

        # }
        # agents_dynanmodb_service.create_item(
        #     item=item
        # )
        # remove local task definition file
        os.remove(created_task_definiton_name_file_path)
        return

    def update_ecs_service(self,
                           task_definition_file_name: str,
                           backend_s3_state_key: str,
                           backend_dynamodb_lock_name):
        print("update ecs service")
        # implementation of update method goes here
        backend_dynanmodb_service = DynamoDBService(
            table_name=backend_dynamodb_lock_name)
        is_table_exist = backend_dynanmodb_service.check_if_table_exist()
        if not is_table_exist:
            raise Exception(
                f"Table {backend_dynamodb_lock_name} does not exist")
        backend_s3_service = S3Service(
            bucket_name=self.backend_s3_bucket_name,
        )

        is_file_exist = backend_s3_service.check_file_exists(
            file_name=backend_s3_state_key)
        if not is_file_exist:
            raise Exception(
                f"File {backend_s3_state_key} does not exist")

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
            backend_dynamodb_lock_name=backend_dynamodb_lock_name,
            backend_region=self.backend_region
        )
        ecs_terraform.terraform_init()
        ecs_terraform.terraform_plan()
        ecs_terraform.terraform_apply()
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
        os.remove(created_task_definiton_name_file_path)
        return

    def delete_ecs_service(
        self,
        backend_s3_state_key,
        backend_dynamodb_lock_name,
        task_definition_file_name,
    ) -> str:
        backend_dynanmodb_service = DynamoDBService(
            table_name=backend_dynamodb_lock_name)
        is_table_exist = backend_dynanmodb_service.check_if_table_exist()
        if not is_table_exist:
            raise Exception(
                f"Table {backend_dynamodb_lock_name} does not exist")
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
            backend_dynamodb_lock_name=backend_dynamodb_lock_name,
            backend_region=self.backend_region
        )
        ecs_terraform.terraform_init()
        ecs_terraform.terraform_destroy()
        os.remove(destination)
        backend_s3_service.remove_file(file_name=backend_s3_state_key)
        return

    def destroy_all_agents(self, backend_s3_state_key_path: str):
        # implementation of destroy method goes here

        backend_s3_service = S3Service(bucket_name=self.backend_s3_bucket_name)
        tfstate_files = backend_s3_service.list_objects(
            path=backend_s3_state_key_path)
        for tf_file in tfstate_files:
            print(tf_file)

        return
    # def _get_agent_info_from_dynamodb_and_s3(self):
    #     # implementation of download method goes here
    #     agents_dynanmodb_service = DynamoDBService(
    #         table_name=self.dynamodb_agents_table_name)
    #     item = agents_dynanmodb_service.get_item(agent_id=self.agent_id)
    #     if len(item) == 0:
    #         raise Exception(f"Agent {self.agent_id} does not exist")
    #     # if yes, download the task definition file from s3
        # s3_service = S3Service(
        #     bucket_name=self.s3_bucket_name_of_task_definition_file,
        # )
    #     task_definition_file_name = item[DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value]
        # source = f"task_definitions/{self.agent_id}/{task_definition_file_name}"
        # destination = f"./terraform/ecs/templates/{task_definition_file_name}"
        # s3_service.download_file(
        #     source=source,
        #     destination=destination
        # )
    #     # if no, raise an error
    #     if not os.path.exists(destination):
    #         raise Exception(
    #             f"Task definition file {task_definition_file_name} does not exist")
    #     # 1. delete ecs service
    #     backend_s3_state_key = item[DynamoDB_Key.BACKEND_S3_STATE_KEY.value]
    #     backend_dynamodb_lock_name = item[DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value]
    #     return backend_s3_state_key, backend_dynamodb_lock_name, task_definition_file_name, destination
