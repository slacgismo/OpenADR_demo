from models_and_classes.TerraformExecution import TerraformExecution
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from models_and_classes.Agent import Agent
import os
import logging
import asyncio


def validate_backend_hcl(file: str, path: str):
    """
    Validate the backend.hcl file
    params: file: str, path: str
    return: None
    """
    file_path = os.path.join(path, file)
    # check if the file exists
    # Todo: check the data

    if not os.path.exists(file_path):
        raise Exception(f"{file_path} does not exist")
    # check the data


def validate_terraform_tfvars(file: str, path: str):
    """ 
    Validate the terraform.tfvars file
    params: file: str, path: str
    return: None
    """
    file_path = os.path.join(path, file)
    # check if the file exists
    # TODO: check the data
    if not os.path.exists(file_path):
        raise Exception(f"{file_path} does not exist")
    # check the data


def parse_message_body(message_body: dict):
    if "agent_id" not in message_body or \
        "resource_id" not in message_body or \
        "market_interval_in_second" not in message_body or \
            "devices" not in message_body:
        raise Exception(
            f"agent_id is not in the message, or resource_id is not in the message, or market_interval_in_second is not in the message, devices is  not in the message")
    agent_id = message_body["agent_id"]
    resource_id = message_body["resource_id"]
    market_interval_in_second = message_body["market_interval_in_second"]
    devices = message_body["devices"]
    return agent_id, resource_id, market_interval_in_second, devices


def handle_action(action: ECS_ACTIONS_ENUM,
                  message_body: dict,
                  BACKEND_S3_BUCKET_NAME: str,
                  DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
                  AWS_REGION: str,

                  ):
    """
    Handle the action from the message body
    params: action: ECS_ACTIONS_ENUM
    params: message_body: dict
    params: BACKEND_S3_BUCKET_NAME: str
    params: DYNAMODB_AGENTS_TABLE_NAME: str
    params: AWS_REGION: str
    return: None
    """
    agent_id, resource_id, market_interval_in_second, devices = parse_message_body(
        message_body)

    task_definition_file_name = f"task-definition-{agent_id}.json.tpl"
    logging.info(
        f"Create task definition file name: {task_definition_file_name}")
    backend_s3_state_key_prefix = f"agent_backend_tfstate"
    backend_s3_state_key = backend_s3_state_key_prefix + f"/{agent_id}-tfstate"

    # create terraofrm execution object
    ecs_terraform = TerraformExecution(
        working_dir="./",
        name_of_creation=f"ecs_service_{agent_id}",
        environment_variables={
            "task_definition_file": task_definition_file_name,
            "agent_id": agent_id
        },
        backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
        backend_s3_state_key=backend_s3_state_key,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        backend_region=AWS_REGION
    )
    # create agent object
    agent = Agent(
        agent_id=agent_id,
        resource_id=resource_id,
        market_interval_in_second=market_interval_in_second,
        devices=devices,
        backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
        s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        backend_region=AWS_REGION,
        terraformExecutionObject=ecs_terraform,
        task_definition_file_name=task_definition_file_name,
        backend_s3_state_key=backend_s3_state_key
    )
    if action == ECS_ACTIONS_ENUM.CREATE.value:
        logging.info("=============================================")
        logging.info(f"Create ecs service {agent_id}")
        logging.info("=============================================")
        if len(devices) == 0:
            # ecs_service.create(is_creating_empty_ecs_service=True)
            # TODO: create empty ecs service
            raise Exception(
                "Not support create empty ecs service, if we need to create empty ecs service. Implement it")
        else:

            logging.info("Create ecs task definition")
            try:
                agent.create_ecs_service(
                )
            except Exception as e:
                # destroy  the dynamodb table just create

                raise Exception(f"Error create ecs task definition: {e}")
        return
    if action == ECS_ACTIONS_ENUM.UPDATE.value:
        logging.info("=============================================")
        logging.info(f"Update ecs service {agent_id}")
        logging.info("=============================================")

        agent.update_ecs_service(
        )
        return
    if action == ECS_ACTIONS_ENUM.DELETE.value:
        logging.info("=============================================")
        logging.info(f"Delete ecs service {agent_id}")
        logging.info("=============================================")

        agent.delete_ecs_service(
        )
        return
