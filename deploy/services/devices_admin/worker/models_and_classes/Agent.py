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
        agents_dynanmodb_service = DynamoDBService(
            table_name=self.dynamodb_agents_table_name)
        # check if the agenet id is already in the dynamodb table
        item = agents_dynanmodb_service.get_item(agent_id=self.agent_id)
        if item is not None and DynamoDB_Key.CURRENT_STATUS.value in item:
            # already exist echeck the satate
            if item[DynamoDB_Key.CURRENT_STATUS.value] != AgentState.DELETED.value:
                raise Exception(
                    f"Agent {self.agent_id} is already active, please use another agent id")
        # update the status of the agent

        # 1. create ecs service

        # if yes, raise an error
        # if no, create a new record in the dynamodb table
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
        # ecs_terraform.terraform_plan()
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

        item = {
            DynamoDB_Key.AGENT_ID.value: self.agent_id,
            DynamoDB_Key.RESOURCE_ID.value: self.resource_id,
            DynamoDB_Key.VTN_ID.value: vtn_id,
            DynamoDB_Key.VENS.value: vens_info,
            DynamoDB_Key.VALID_AT.value: str(int(time.time())),
            DynamoDB_Key.BACKEND_S3_STATE_KEY.value: backend_s3_state_key,
            DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value: backend_dynamodb_lock_name,
            DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value: task_definition_file_name,
            DynamoDB_Key.CURRENT_STATUS.value: AgentState.ACTIVE.value

        }

        if item[DynamoDB_Key.CURRENT_STATUS.value] == AgentState.DELETED.value:
            # update the agent record in the dynamodb table
            print("update the deleted agent record in the dynamodb table")
            agents_dynanmodb_service.upate_items(agent_id=self.agent_id,
                                                 update_keys_values=item,
                                                 remove_keys=None)
        else:
            # create the agent record in the dynamodb table
            agents_dynanmodb_service.create_item(
                item=item
            )
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
        agents_dynanmodb_service = DynamoDBService(
            table_name=self.dynamodb_agents_table_name)
        agent_record = agents_dynanmodb_service.get_item(
            agent_id=self.agent_id)

        if agent_record is None:
            # raise exception if the agent id exist in the dynamodb table, please use another agent id
            raise Exception(
                f"Agent {self.agent_id} does not exist, please use create method")

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
        # ecs_terraform.terraform_plan()
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
        # update the agent record in the dynamodb table
        item = {
            DynamoDB_Key.RESOURCE_ID.value: self.resource_id,
            DynamoDB_Key.VTN_ID.value: vtn_id,
            DynamoDB_Key.VENS.value: vens_info,
            DynamoDB_Key.BACKEND_S3_STATE_KEY.value: backend_s3_state_key,
            DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value: backend_dynamodb_lock_name,
            DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value: task_definition_file_name,
            DynamoDB_Key.CURRENT_STATUS.value: AgentState.ACTIVE.value

        }
        print(f"item: {item}")
        # check if the agenet id is already in the dynamodb table

        if len(agent_record) > 0:
            print("update the deleted agent record in the dynamodb table")
            agents_dynanmodb_service.upate_items(agent_id=self.agent_id,
                                                 update_keys_values=item
                                                 )
        else:
            raise Exception(
                f"Agent {self.agent_id} does not exist in the dynamodb table {self.dynamodb_agents_table_name}")
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
        agents_dynanmodb_service = DynamoDBService(
            table_name=self.dynamodb_agents_table_name)
        agent_record = agents_dynanmodb_service.get_item(
            agent_id=self.agent_id)
        print("agent_record = ", agent_record)
        if agent_record is None:
            # raise exception if the agent id exist in the dynamodb table, please use another agent id
            raise Exception(
                f"Agent {self.agent_id} does not exist, please use create method")

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
            backend_dynamodb_lock_name=backend_dynamodb_lock_name,
            backend_region=self.backend_region
        )
        ecs_terraform.terraform_init()
        ecs_terraform.terraform_destroy()
        os.remove(destination)
        backend_s3_service.remove_file(file_name=backend_s3_state_key)

        # update the agent record in the dynamodb table

        item = {

            DynamoDB_Key.CURRENT_STATUS.value: AgentState.DELETED.value,

        }
        # update the agent record in the dynamodb table
        agents_dynanmodb_service.upate_items(agent_id=self.agent_id,
                                             update_keys_values=item)
        # remvoe the keys from the dynamodb table to indicate that the agent is deleted
        keys_to_remove = [DynamoDB_Key.RESOURCE_ID.value,
                          DynamoDB_Key.VTN_ID.value,
                          DynamoDB_Key.VENS.value,
                          DynamoDB_Key.BACKEND_S3_STATE_KEY.value,
                          DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value,
                          DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value,
                          ]
        agents_dynanmodb_service.remove_keys_from_item(
            agent_id=self.agent_id,
            keys_to_remove=keys_to_remove
        )

        return
