import urllib.parse
import socketserver
import http.server
import boto3
import os
import json
import uuid
from typing import List, Dict, Tuple
from enum import Enum
# from helper.task_definition_generator import create_and_export_task_definition, VTN_TASK_VARIANTS_ENUM, VEN_TASK_VARIANTS_ENUM
# from models_and_classes.TerraformDynamodbLockTable import TerraformDynamodbLockTable
import time
import configparser
from models_and_classes.TerraformExecution import TerraformExecution
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
# from models_and_classes.S3Service import S3Service
from models_and_classes.Agent import Agent, AgentState
from models_and_classes.DynamoDBService import DynamoDBService, DynamoDB_Key
from models_and_classes.S3Service import S3Service
FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")
BACKEND_S3_BUCKET_NAME = os.getenv('backend_s3_bucket_devices_admin')
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")

DYNAMODB_AGENTS_TABLE_NAME = os.getenv('dynamodb_agents_table_name')
if DYNAMODB_AGENTS_TABLE_NAME is None:
    raise Exception("DYNAMODB_AGENTS_TABLE_NAME is not set")


AWS_REGION = os.getenv('aws_region')
if AWS_REGION is None:
    raise Exception("AWS_REGION is not set")

# Select the table
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def get_agent_info_from_dynamodb_and_s3(
    agent_id: str,
    dynamodb_agents_table_name: str,
    backend_s3_bucket_name: str,
    s3_bucket_name_of_task_definition_file
):
    # implementation of download method goes here
    agents_dynanmodb_service = DynamoDBService(
        table_name=dynamodb_agents_table_name)
    item = agents_dynanmodb_service.get_item(agent_id=agent_id)
    if len(item) == 0:
        raise Exception(f"Agent {agent_id} does not exist")
    # if yes, download the task definition file from s3
    s3_service = S3Service(
        bucket_name=s3_bucket_name_of_task_definition_file,
    )
    task_definition_file_name = item[DynamoDB_Key.TASK_DEFINITION_FILE_NAME.value]
    source = f"task_definitions/{self.agent_id}/{task_definition_file_name}"
    destination = f"./terraform/ecs/templates/{task_definition_file_name}"
    s3_service.download_file(
        source=source,
        destination=destination
    )
    # if no, raise an error
    if not os.path.exists(destination):
        raise Exception(
            f"Task definition file {task_definition_file_name} does not exist")
    # 1. delete ecs service
    backend_s3_state_key = item[DynamoDB_Key.BACKEND_S3_STATE_KEY.value]
    backend_dynamodb_lock_name = item[DynamoDB_Key.BACKEND_DYNAMODB_LOCK_NAME.value]
    return backend_s3_state_key, backend_dynamodb_lock_name, task_definition_file_name, destination


def create_terraform_dynamondb_lock_table(dyanmodb_table_name: str):

    terrafrom_execution = TerraformExecution(
        working_dir="./terraform",
        name_of_creation="dynamodb",
        environment_variables=(
            {"backend_dyanmodb_table_teraform_state_lock_devices_admin": dyanmodb_table_name})
    )
    try:
        # init terraform
        terrafrom_execution.terraform_init()
        # optional validate
        terrafrom_execution.terraform_validate()
        # optional plan
        terrafrom_execution.terraform_plan()
    except Exception as e:
        raise Exception(f"Error validate dynamodb table from terraform: {e}")
        # apply --auto-approve

    try:
        terrafrom_execution.terraform_apply()
    except Exception as e:
        # apply --auto-approve
        print("Error creating dynamodb table from terraform, destroying the table")
        print("Destroying the table")
        terrafrom_execution.terraform_destroy()
        raise Exception(f"Error creating dynamodb table from terraform: {e}")


def destroy_terraform_dynamondb_lock_table(dyanmodb_table_name: str):
    terrafrom_execution = TerraformExecution(
        working_dir="./terraform",
        name_of_creation="dynamodb",
        environment_variables=(
            {"backend_dyanmodb_table_teraform_state_lock_devices_admin": dyanmodb_table_name})
    )
    try:
        # init terraform
        terrafrom_execution.terraform_init()
        terrafrom_execution.terraform_destroy()
    except Exception as e:
        raise Exception(f"Error validate dynamodb table from terraform: {e}")
        # apply --auto-approve


def validate_backend_hcl(file: str, path: str):
    file_path = os.path.join(path, file)
    # check if the file exists

    if not os.path.exists(file_path):
        raise Exception(f"{file_path} does not exist")
    # check the data


def validate_terraform_tfvars(file: str, path: str):
    file_path = os.path.join(path, file)
    # check if the file exists
    if not os.path.exists(file_path):
        raise Exception(f"{file_path} does not exist")
    # check the data


def parse_message_body(message_body: dict):
    if "agent_id" not in message_body or \
        "resource_id" not in message_body or \
        "market_interval_in_second" not in message_body or \
            "devices" not in message_body:
        raise Exception(
            f"agent_id is not in the message, or resource_id is not in the message, \
                    or market_interval_in_second is not in the message, devices is \
                        not in the message")
    agent_id = message_body["agent_id"]
    resource_id = message_body["resource_id"]
    market_interval_in_second = message_body["market_interval_in_second"]
    devices = message_body["devices"]
    return agent_id, resource_id, market_interval_in_second, devices


def handle_action(action: ECS_ACTIONS_ENUM, message_body: dict):

    agent_id, resource_id, market_interval_in_second, devices = parse_message_body(
        message_body)

    task_definition_file_name = f"task-definition-{agent_id}.json.tpl"
    print("Create task definition file name: ", task_definition_file_name)
    backend_dyanmodb_agent_lock_state = f"{agent_id}-state-lock-tfstate"
    backend_s3_state_key_prefix = f"agent.backend.tfstate"
    backend_s3_state_key = backend_s3_state_key_prefix + f"/{agent_id}-tfstate"
    print("Create dynamodb table lock name: ",
          backend_dyanmodb_agent_lock_state)

    if action == ECS_ACTIONS_ENUM.CREATE.value:
        if len(devices) == 0:
            # ecs_service.create(is_creating_empty_ecs_service=True)
            print("create empty ecs service")
        else:

            try:
                validate_backend_hcl(file="backend.hcl",
                                     path="./terraform")
                validate_terraform_tfvars(
                    file="terraform.tfvars", path="./terraform")
                # check if the agent_id is already in the dynamodb table

            except Exception as e:
                raise Exception(f"Error validate necessary files : {e}")
            # check the if backend.hcl is correct

            # create the dynamodb table lock for terraform
            create_terraform_dynamondb_lock_table(
                dyanmodb_table_name=backend_dyanmodb_agent_lock_state)
            print("=============================")
            print("End of create dynamodb table lock")
            # end of create dynamodb table lock

            print("Create ecs task definition")
            agent = Agent(
                agent_id=agent_id,
                resource_id=resource_id,
                market_interval_in_second=market_interval_in_second,
                devices=devices,
                backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
                s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
                dynamodb_agents_table_name=DYNAMODB_AGENTS_TABLE_NAME,
                backend_region=AWS_REGION
            )
            agent.create_ecs_service(
                task_definition_file_name=task_definition_file_name,
                backend_s3_state_key=backend_s3_state_key,
                backend_dynamodb_lock_name=backend_dyanmodb_agent_lock_state
            )
        return
    if action == ECS_ACTIONS_ENUM.UPDATE.value:
        print("Update")
        agent = Agent(
            agent_id=agent_id,
            resource_id=resource_id,
            market_interval_in_second=market_interval_in_second,
            devices=devices,
            backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
            s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
            dynamodb_agents_table_name=DYNAMODB_AGENTS_TABLE_NAME,
            backend_region=AWS_REGION
        )
        agent.update_ecs_service(
            task_definition_file_name=task_definition_file_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=backend_dyanmodb_agent_lock_state
        )
        return
    if action == ECS_ACTIONS_ENUM.DELETE.value:

        agent = Agent(
            agent_id=agent_id,
            resource_id=resource_id,
            market_interval_in_second=market_interval_in_second,
            devices=devices,
            backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
            s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
            dynamodb_agents_table_name=DYNAMODB_AGENTS_TABLE_NAME,
            backend_region=AWS_REGION
        )
        agent.delete_ecs_service(
            task_definition_file_name=task_definition_file_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=backend_dyanmodb_agent_lock_state
        )
        destroy_terraform_dynamondb_lock_table(
            dyanmodb_table_name=backend_dyanmodb_agent_lock_state
        )
        return

    if action == ECS_ACTIONS_ENUM.DESTROY_ALL.value:
        agent = Agent(
            agent_id=agent_id,
            resource_id=resource_id,
            market_interval_in_second=market_interval_in_second,
            devices=devices,
            backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
            s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
            dynamodb_agents_table_name=DYNAMODB_AGENTS_TABLE_NAME,
            backend_region=AWS_REGION
        )
        agent.destroy_all_agents(
            backend_s3_state_key_path=backend_s3_state_key_prefix)


def process_task_from_fifo_sqs(queue_url, MaxNumberOfMessages: int = 1, WaitTimeSeconds: int = 5, VisibilityTimeout: int = 5):
    sqs = boto3.client('sqs')
    while True:
        # Check if there are any messages in the queue
        print("start to receive message at %s" % str(time.time()))
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=MaxNumberOfMessages,
            WaitTimeSeconds=WaitTimeSeconds,
            VisibilityTimeout=VisibilityTimeout,
            ReceiveRequestAttemptId=str(time.time())
        )

        # If no messages, exit loop
        if 'Messages' not in response:
            print("No message received at %s" % str(time.time()))

            time.sleep(1)
            break
        else:
            # Process the message
            message = response['Messages'][0]
            print('Received message: %s' % message['Body'])

            # Wait for task to finish before pulling next message
            # check the sqs title attribute to see the task action
            message_attributes = message['MessageAttributes']
            action = message_attributes['Action']['StringValue']
            message_body = json.loads(message['Body'])
            # handle_action(action, message_body)
            handle_action(action=ECS_ACTIONS_ENUM.DESTROY_ALL.value,
                          message_body=message_body)

            print("end to receive message at %s" % str(time.time()))
            break
            time.sleep(1)


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


if __name__ == '__main__':
    # poll message from a fifo sqs
    process_task_from_fifo_sqs(
        queue_url=FIFO_SQS_URL)
