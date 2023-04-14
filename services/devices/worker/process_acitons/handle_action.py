import os
import logging

from classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from classes.TerraformExecution import TerraformExecution
from classes.S3Service import S3Service
from classes.Agent import Agent
from pathlib import Path
from .task_definition_generator import create_vtn_params, VariablesDefinedInTerraform, create_ven_params, generate_vtn_task_definition, CONTAINER_DEFINITION_TEMPLATE, generate_ven_task_definition, combine_vtn_and_vens_as_task_definition, export_to_json_tpl, create_new_task_definition, insert_device_to_existing_task_defintion_file, remove_device_from_task_definition_file, is_any_device_exist_in_task_definition_file
from enum import Enum
import json


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
    """
    {
    "eventName": "INSERT",
    "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
    "resource_id": "caff6719c24359a155a4d0d2f265a7",
    "market_interval_in_seconds": "300",
    "device_id": "807f8e4a37446e80c5756a74a3598d",
    "device_type": "ES",
    "meter_id": "6436a67e184d3694a15886215ae464"
    "device_settings": {
        "battery_token": "12321321qsd",
        "battery_sn": "66354",
        "device_brand": "SONNEN_BATTERY"
        "is_using_mock_device": true
        "flexible": "1",
    }

    }
    """
    try:
        agent_id = message_body["agent_id"]
        resource_id = message_body["resource_id"]
        market_interval_in_seconds = message_body["market_interval_in_seconds"]
        device_id = message_body["device_id"]
        device_type = message_body["device_type"]
        meter_id = message_body["meter_id"]
        device_settings = message_body["device_settings"]
        return agent_id, resource_id, market_interval_in_seconds, device_id, device_type, meter_id, device_settings
    except Exception as e:
        raise Exception(f"Error parsing message body: {e}")


def handle_action(
    action: ECS_ACTIONS_ENUM,
    message_body: dict,
    BACKEND_S3_BUCKET_NAME: str,
    DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME: str,
    AWS_REGION: str,
    # METER_API_URL: str,
    # DEVICES_API_URL: str,
    # ORDERS_API_URL: str,
    # DISPATCHES_API_URL: str,
    # EMULATED_DEVICE_API_URL: str,
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
    agent_id, resource_id, market_interval_in_seconds, device_id, device_type, meter_id, device_settings = parse_message_body(
        message_body
    )

    task_definition_file_name = f"task-definition-{agent_id}.json.tpl"
    logging.info(
        f"Create task definition file name: {task_definition_file_name}")
    backend_s3_state_key_prefix = f"agent_backend_tfstate"
    backend_s3_state_key = backend_s3_state_key_prefix + f"/{agent_id}-tfstate"

    worker_path = Path(__file__).parent.parent
    terrafrom_abs_path = os.path.join(worker_path, "terraform")

    # create terraofrm execution object
    ecs_terraform = TerraformExecution(
        working_dir=terrafrom_abs_path,
        name_of_creation=f"ecs_service_{agent_id}",
        environment_variables={
            "task_definition_file": task_definition_file_name,
            "agent_id": agent_id,
        },
        backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
        backend_s3_state_key=backend_s3_state_key,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        backend_region=AWS_REGION,
    )
    s3_service = S3Service(
        bucket_name=BACKEND_S3_BUCKET_NAME,
    )
    # ==============================
    # Create task definition file
    # ==============================

    # step 1: check the task definition file is exist on S3
    s3_source = f"task_definitions/{agent_id}/{task_definition_file_name}"
    local_path = "./terraform/templates"
    destination = local_path + f"/{task_definition_file_name}"
    is_file_exist = s3_service.check_file_exists(file_name=s3_source)
    logging.info("=== Check if the task definition file exists on S3 ===")

    if action == ECS_ACTIONS_ENUM.INSERT.value:
        if not is_file_exist:
            # create task definition file
            logging.info("=== Create a new task definition file ==")
            # create vtn container
            create_new_task_definition(
                market_interval_in_seconds=market_interval_in_seconds,
                agent_id=agent_id,
                resource_id=resource_id,
                device_id=device_id,
                device_type=device_type,
                meter_id=meter_id,
                device_settings=device_settings,
                local_file_destination=destination,
            )

        else:
            logging.info("=== Insert the existing task definition file ==")
            s3_service.download_file(source=s3_source, destination=destination)
            #  modeify existing task definition file
            insert_device_to_existing_task_defintion_file(
                market_interval_in_seconds=market_interval_in_seconds,
                agent_id=agent_id,
                resource_id=resource_id,
                device_id=device_id,
                device_type=device_type,
                meter_id=meter_id,
                device_settings=device_settings,
                local_file_destination=destination,
            )

    if action == ECS_ACTIONS_ENUM.MODIFY.value:
        raise Exception(
            "Modify action should not be used, check the code that send the message")

    if action == ECS_ACTIONS_ENUM.REMOVE.value:
        logging.info("== Remove device from agent with device == ")
        if not is_file_exist:
            raise Exception(
                "Task definition file is not exist with REMOVE action")
        else:
            s3_service.download_file(source=s3_source, destination=destination)
            remove_device_from_task_definition_file(
                agent_id=agent_id,
                device_id=device_id,
                local_file_destination=destination,
            )
    # check if this is a empty service with no device
    is_any_device_exist = is_any_device_exist_in_task_definition_file(
        file_path=destination,
    )
    # =================
    # execute terraform
    # =================
    if not is_any_device_exist:
        # remove ecs service

        ecs_terraform.terraform_init()
        ecs_terraform.terraform_destroy()
        logging.info("========================================")
        logging.info(f"ECS service destroied: {agent_id}")
        logging.info("========================================")

    else:
        logging.info(
            "===  Creare or Update the ecs service ===")
        ecs_terraform.terraform_init()
        # ecs_terraform.terraform_plan()
        ecs_terraform.terraform_apply()
        logging.info("========================================")
        logging.info(f"ECS service updated: {agent_id}")
        logging.info("========================================")

    s3_service.upload_file(source=destination, destination=s3_source)
    logging.info(f"=== Upload the task definition file to S3 :{s3_source} ===")
    # remove local task definition file
    os.remove(destination)
