import urllib.parse
import socketserver
import http.server
import boto3
import os
import json
import uuid

from enum import Enum
from helper.task_definition_generator import create_and_export_task_definition, VTN_TASK_VARIANTS_ENUM, VEN_TASK_VARIANTS_ENUM
from ecs.TerraformDynamodbLockTable import TerraformDynamodbLockTable
import time
from ecs.ECSService import ECSService
from ecs.ECSTaskDefinitions import ECSTaskDefinitions
from ecs.S3Service import S3Service


class ECS_ACTIONS_ENUM(Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"


class ECS_CLUSTER_PARAMS_ENUM(Enum):
    AWS_REGION = "AWS_REGION"
    ECS_CLUSTER_NAME = "ECS_CLUSTER_NAME"
    FIFO_SQS_URL = "FIFO_SQS_URL"
    PRIVATE_SG_NAME = "PRIVATE_SG_NAME"
    ECS_TASK_EXECUTION_ROLE_NAME = "ECS_TASK_EXECUTION_ROLE_NAME"
    ECS_TASK_ROLE_NAME = "ECS_TASK_ROLE_NAME"
    PRIVATE_VPC_ID = "PRIVATE_VPC_ID"
    CLOUDWATCH_NAME = "CLOUDWATCH_NAME"
    BACKEND_S3_BUCKET_NAME = "BACKEND_S3_BUCKET_NAME"
    BACKEND_S3_BUCKET_KEY = "BACKEND_S3_BUCKET_KEY"
    BACKEND_REGION = "BACKEND_REGION"
    BACKEND_DYNAMODB_TABLE_NAME = "BACKEND_DYNAMODB_TABLE_NAME"
    APP_IMAGE_VTN = "APP_IMAGE_VTN"
    APP_IMAGE_VEN = "APP_IMAGE_VEN"


class TAG_PARAMS_ENUM(Enum):
    PROJECT = "PROJECT"
    PREFIX = "PREFIX"
    CREATOR = "CREATOR"
    MANAGED_BY = "MANAGED_BY"


# Environment from the main system that generated from Terraform
# VTN image environment variables
# PROD or DEV (PROD: real device, DEV: mock device)
VTN_ENV_VARIANTS = os.getenv('VEN_TASK_VARIANTS') or {

    "SAVE_DATA_URL": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices",
    "GET_VENS_URL": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/openadr_devices",
    "MARKET_PRICES_URL": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/market_prices",
    "PARTICIPATED_VENS_URL": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/participated_vens",
}

SAVE_DATA_URL = VTN_ENV_VARIANTS[VTN_TASK_VARIANTS_ENUM.SAVE_DATA_URL.value]
GET_VENS_URL = VTN_ENV_VARIANTS[VTN_TASK_VARIANTS_ENUM.GET_VENS_URL.value]
MARKET_PRICES_URL = VTN_ENV_VARIANTS[VTN_TASK_VARIANTS_ENUM.MARKET_PRICES_URL.value]
PARTICIPATED_VENS_URL = VTN_ENV_VARIANTS[VTN_TASK_VARIANTS_ENUM.PARTICIPATED_VENS_URL.value]


# VEN image environment variables
VEN_ENV_VARIANTS = os.getenv('VTN_TASK_VARIANTS') or {

    "MOCK_DEVICES_API_URL": "https://l19grkzsyk.execute-api.us-east-2.amazonaws.com/dev/battery_api",
    "VTN_ADDRESS": "127.0.0.1",
    "VTN_PORT": "8080",
}

MOCK_DEVICES_API_URL = VEN_ENV_VARIANTS[VEN_TASK_VARIANTS_ENUM.MOCK_DEVICES_API_URL.value]
VTN_ADDRESS = VEN_ENV_VARIANTS[VEN_TASK_VARIANTS_ENUM.VTN_ADDRESS.value]
VTN_PORT = VEN_ENV_VARIANTS[VEN_TASK_VARIANTS_ENUM.VTN_PORT.value]

ENV = os.getenv('ENV') or "DEV"

# ECS cluster params that had beed pre-configed in the main system
ECS_CLUSTER_PARAMS = os.getenv("ECS_CLUSTER_PARAMS") or {
    "AWS_REGION": "us-east-2",
    "ECS_CLUSTER_NAME": "openadr-dev-agents-cluster",
    "FIFO_SQS_URL": "https://sqs.us-east-2.amazonaws.com/041414866712/openadr_workers_sqs.fifo",
    "PRIVATE_SG_NAME": "public-bastion-sg-20230311232022989900000002",
    "ECS_TASK_EXECUTION_ROLE_NAME": "openadr-task-exec-role",
    "ECS_TASK_ROLE_NAME": "openadr-vtn-task",
    "PRIVATE_VPC_ID": "vpc-012a219f9778e1158",
    "CLOUDWATCH_NAME": "openadr-ecs-agent",
    "BACKEND_S3_BUCKET_NAME": "openadr-agents-state",
    "BACKEND_S3_BUCKET_KEY": "openadr-dev-devices_admin.tfstate",
    "BACKEND_REGION": "us-east-2",
    "BACKEND_DYNAMODB_TABLE_NAME":  "openadr-devices-admin-tf-state-lock",
    "APP_IMAGE_VTN": "041414866712.dkr.ecr.us-east-2.amazonaws.com/vtn:latest",
    "APP_IMAGE_VEN": "041414866712.dkr.ecr.us-east-2.amazonaws.com/ven:latest",
}
PRIVATE_VPC_ID = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.PRIVATE_VPC_ID.value]
PRIVATE_SG_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.PRIVATE_SG_NAME.value]
ECS_TASK_ROLE_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.ECS_TASK_ROLE_NAME.value]
ECS_TASK_EXECUTION_ROLE_NAME = ECS_CLUSTER_PARAMS[
    ECS_CLUSTER_PARAMS_ENUM.ECS_TASK_EXECUTION_ROLE_NAME.value]
ECS_CLUSTER_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.ECS_CLUSTER_NAME.value]
BACKEND_S3_BUCKET_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.BACKEND_S3_BUCKET_NAME.value]
BACKEND_S3_BUCKET_KEY = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.BACKEND_S3_BUCKET_KEY.value]
BACKEND_REGION = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.BACKEND_REGION.value]
BACKEND_DYNAMODB_TABLE_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.BACKEND_DYNAMODB_TABLE_NAME.value]

APP_IMAGE_VTN = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.APP_IMAGE_VTN.value]
APP_IMAGE_VEN = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.APP_IMAGE_VEN.value]
CLOUDWATCH_NAME = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.CLOUDWATCH_NAME.value]
AWS_REGION = ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.AWS_REGION.value]
# # Environment from the main system that generated from Terraform
TAG_PARAMS = os.getenv("TAG_PARAMS") or {
    "PROJECT": "openadr",
    "PREFIX": "openadr-dev-agents",
    "CREATOR": "Jimmy",
    "MANAGED_BY": "Terraform",
}
PROJECT = TAG_PARAMS[TAG_PARAMS_ENUM.PROJECT.value]
PREFIX = TAG_PARAMS[TAG_PARAMS_ENUM.PREFIX.value]
CREATOR = TAG_PARAMS[TAG_PARAMS_ENUM.CREATOR.value]
MANAGED_BY = TAG_PARAMS[TAG_PARAMS_ENUM.MANAGED_BY.value]

# VTN envirornmant variables


# VEN envirornmant variables


# Select the table
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def create_ecs_auto_tfvars_params(task_definition_name_file_name: str, agent_id: str) -> dict:
    terraform_auto_tfvars_params = dict()
    terraform_auto_tfvars_params['aws_region'] = AWS_REGION
    terraform_auto_tfvars_params['environment'] = ENV
    terraform_auto_tfvars_params['project'] = PROJECT
    terraform_auto_tfvars_params['prefix'] = PREFIX
    terraform_auto_tfvars_params['creator'] = CREATOR
    terraform_auto_tfvars_params['managedBy'] = MANAGED_BY
    terraform_auto_tfvars_params['task_definition_file'] = os.path.join(
        "./templates", task_definition_name_file_name)
    terraform_auto_tfvars_params['agent_id'] = agent_id
    terraform_auto_tfvars_params['cloudwatch_name'] = CLOUDWATCH_NAME
    terraform_auto_tfvars_params['ecs_cluster_name'] = ECS_CLUSTER_NAME
    terraform_auto_tfvars_params['ecs_task_execution_role_name'] = ECS_TASK_EXECUTION_ROLE_NAME
    terraform_auto_tfvars_params['ecs_task_role_name'] = ECS_TASK_ROLE_NAME
    terraform_auto_tfvars_params['private_sg_name'] = PRIVATE_SG_NAME
    terraform_auto_tfvars_params['private_vpc_id'] = PRIVATE_VPC_ID
    return terraform_auto_tfvars_params


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
    ecs_service = ECSService(
        agent_id=agent_id,
        resource_id=resource_id,
        market_interval_in_second=market_interval_in_second,
    )
    task_definition_name_file_name = f"task-definition-{agent_id}.json.tpl"
    ECSBackendDynamoDBLockName = f"{agent_id}-state-lock-tfstate"
    if action == ECS_ACTIONS_ENUM.CREATE.value:
        if len(devices) == 0:
            ecs_service.create(is_creating_empty_ecs_service=True)
        else:
            # step 1 create a dynamodb table lock for the agent
            terraform_dynamodb_lock = TerraformDynamodbLockTable(
                path="./terraform_dynamodb",
                backend_hcl_filename="backend.hcl",
                backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
                backend_s3_key=BACKEND_S3_BUCKET_KEY,
                backend_region=BACKEND_REGION,
                backend_dynamodb_table=BACKEND_DYNAMODB_TABLE_NAME)

            terraform_auto_tfvars_params_dynamodb = {
                "aws_region": AWS_REGION,
                "environment": ENV,
                "project": PROJECT,
                "prefix": PREFIX,
                "creator": CREATOR,
                "managedBy": MANAGED_BY,
                "ECSBackendDynamoDBLockName": ECSBackendDynamoDBLockName
            }
            terraform_dynamodb_lock.create(
                terraform_auto_tfvars_file_name="terraform.auto.tfvars",
                terraform_auto_tfvars_params=terraform_auto_tfvars_params_dynamodb)
            print("=============================")
            # end of create dynamodb table lock
            print("Create ecs task definition")
            # task_definition_name_file_name = f"task-definition-{agent_id}.json.tpl"
            created_task_definiton_name_file_path = create_and_export_task_definition(
                agent_id=agent_id,
                resource_id=resource_id,
                market_interval_in_second=market_interval_in_second,
                devices=devices,
                env=ENV,
                save_data_url=SAVE_DATA_URL,
                get_vens_url=GET_VENS_URL,
                participated_vens_url=PARTICIPATED_VENS_URL,
                app_image_vtn=APP_IMAGE_VTN,
                app_image_ven=APP_IMAGE_VEN,
                log_group_name=CLOUDWATCH_NAME,
                aws_region=AWS_REGION,
                mock_devices_api_url=MOCK_DEVICES_API_URL,
                vtn_address=VTN_ADDRESS,
                vtn_port=VTN_PORT,
                market_prices_url=MARKET_PRICES_URL,
                file_name=task_definition_name_file_name,
                path="./terraform_ecs/templates"

            )
            # save task definition file to S3
            s3_service = S3Service(
                bucket_name=BACKEND_S3_BUCKET_NAME,

            )

            s3_service.upload_file(
                source=created_task_definiton_name_file_path,
                destination=f"task_definitions/{agent_id}/{task_definition_name_file_name}"
            )
            # print("task_defition_file ", task_defition_file)
            # create backend.hcl
            ecs_service.creagte_backend_hcl_file(
                path="./terraform_ecs",
                backend_hcl_filename="backend.hcl",
                backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
                backend_s3_key=f"{PREFIX}-{agent_id}-{ENV}.tfstate",
                backend_region=BACKEND_REGION,
                backend_dynamodb_table=ECSBackendDynamoDBLockName
            )
            # create terraform.auto.tfvars
            ecs_terraform_auto_tfvars_params = create_ecs_auto_tfvars_params(
                task_definition_name_file_name=task_definition_name_file_name,
                agent_id=agent_id,
            )

            ecs_service.create_terraform_auto_tfvars_file(
                path="./terraform_ecs",
                terraform_auto_tfvars_file_name="terraform.auto.tfvars",
                params=ecs_terraform_auto_tfvars_params
            )
            ecs_service.create(is_creating_empty_ecs_service=False)

    elif action == ECS_ACTIONS_ENUM.UPDATE.value:
        print("Update")
        # task_definition_name_file_name = f"task-definition-{agent_id}.json.tpl"
        created_task_definiton_name_file_path = create_and_export_task_definition(
            agent_id=agent_id,
            resource_id=resource_id,
            market_interval_in_second=market_interval_in_second,
            devices=devices,
            env=ENV,
            save_data_url=SAVE_DATA_URL,
            get_vens_url=GET_VENS_URL,
            participated_vens_url=PARTICIPATED_VENS_URL,
            app_image_vtn=APP_IMAGE_VTN,
            app_image_ven=APP_IMAGE_VEN,
            log_group_name=CLOUDWATCH_NAME,
            aws_region=AWS_REGION,
            mock_devices_api_url=MOCK_DEVICES_API_URL,
            vtn_address=VTN_ADDRESS,
            vtn_port=VTN_PORT,
            market_prices_url=MARKET_PRICES_URL,
            file_name=task_definition_name_file_name,
            path="./terraform_ecs/templates"

        )
        # save task definition file to S3
        s3_service = S3Service(
            bucket_name=BACKEND_S3_BUCKET_NAME,

        )

        s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{agent_id}/{task_definition_name_file_name}"
        )
        # print("task_defition_file ", task_defition_file)
        # create backend.hcl
        ecs_service.creagte_backend_hcl_file(
            path="./terraform_ecs",
            backend_hcl_filename="backend.hcl",
            backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
            backend_s3_key=f"{PREFIX}-{agent_id}-{ENV}.tfstate",
            backend_region=BACKEND_REGION,
            backend_dynamodb_table=ECSBackendDynamoDBLockName
        )
        # create terraform.auto.tfvars
        ecs_terraform_auto_tfvars_params = create_ecs_auto_tfvars_params(
            task_definition_name_file_name=task_definition_name_file_name,
            agent_id=agent_id,
        )

        ecs_service.create_terraform_auto_tfvars_file(
            path="./terraform_ecs",
            terraform_auto_tfvars_file_name="terraform.auto.tfvars",
            params=ecs_terraform_auto_tfvars_params
        )
        ecs_service.create(is_creating_empty_ecs_service=False)
    elif action == ECS_ACTIONS_ENUM.DELETE.value:
        print("DELETE ECS SERVICE")
        s3_service = S3Service(
            bucket_name=BACKEND_S3_BUCKET_NAME,
        )
        # create backend.hcl
        ecs_service.creagte_backend_hcl_file(
            path="./terraform_ecs",
            backend_hcl_filename="backend.hcl",
            backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
            backend_s3_key=f"{PREFIX}-{agent_id}-{ENV}.tfstate",
            backend_region=BACKEND_REGION,
            backend_dynamodb_table=ECSBackendDynamoDBLockName
        )
        # create terraform.auto.tfvars
        ecs_terraform_auto_tfvars_params = create_ecs_auto_tfvars_params(
            task_definition_name_file_name=task_definition_name_file_name,
            agent_id=agent_id,
        )

        task_definition_name_file_path = s3_service.downlo_file(
            source=f"task_definitions/{agent_id}/{task_definition_name_file_name}",
            destination=f"./terraform_ecs/templates/{task_definition_name_file_name}"
        )
        ecs_service.delete()

    else:
        print("Action not supported")


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
            handle_action(action, message_body)
            handle_action(action=ECS_ACTIONS_ENUM.DELETE.value,
                          message_body=message_body)
            # Delete the message from the queue
            # sqs.delete_message(
            #     QueueUrl=queue_url,
            #     ReceiptHandle=message['ReceiptHandle']
            # )
            print("end to receive message at %s" % str(time.time()))
            break
            time.sleep(1)


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


if __name__ == '__main__':
    # poll message from a fifo sqs
    process_task_from_fifo_sqs(
        queue_url=ECS_CLUSTER_PARAMS[ECS_CLUSTER_PARAMS_ENUM.FIFO_SQS_URL.value])
