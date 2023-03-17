import urllib.parse
import socketserver
import http.server
import boto3
import os
import json
import uuid

from enum import Enum
from helper.task_definition_generator import create_and_export_task_definition, VTN_TASK_VARIANTS_ENUM, VEN_TASK_VARIANTS_ENUM
# from models_and_classes.TerraformDynamodbLockTable import TerraformDynamodbLockTable
import time
# from ecs.ECSService import ECSService
# from ecs.ECSTaskDefinitions import ECSTaskDefinitions
# from ecs.S3Service import S3Service
import configparser
from models_and_classes.TerraformExecution import TerraformExecution
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from models_and_classes.S3Service import S3Service


FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
if FIFO_SQS_URL is None:
    raise Exception("FIFO_SQS_URL is not set")
BACKEND_S3_BUCKET_NAME = os.getenv('backend_s3_bucket_devices_admin')
if BACKEND_S3_BUCKET_NAME is None:
    raise Exception("BACKEND_S3_BUCKET_NAME is not set")
# Select the table
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def create_terraform_ecs(task_definition_file_name: str, agent_id: str):
    ecs_terraform = TerraformExecution(
        working_dir="./terraform/ecs",
        name_of_creation=f"ecs-service-{agent_id}",

        environment_variables={
            "task_definition_file": task_definition_file_name,
            "agent_id": agent_id
        }
    )

    try:
        # init terraform
        ecs_terraform.terraform_init()
        # optional validate
        ecs_terraform.terraform_validate()
        # optional plan
        ecs_terraform.terraform_plan()
    except Exception as e:
        raise Exception(f"Error validate ecs service from terraform: {e}")
        # apply --auto-approve

    try:
        print("apply ecs service")
        ecs_terraform.terraform_apply()
    except Exception as e:
        # apply --auto-approve
        print("Error creating ecs service from terraform")
        print("Destroying the esc service")
        ecs_terraform.terraform_destroy()
        raise Exception(f"Error creating ecs service from terraform: {e}")


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

    task_definition_name_file_name = f"task-definition-{agent_id}.json.tpl"
    print("Create task definition file name: ", task_definition_name_file_name)
    backend_dyanmodb_table_teraform_state_lock_devices_admin = f"{agent_id}-state-lock-tfstate"
    print("Create dynamodb table lock name: ",
          backend_dyanmodb_table_teraform_state_lock_devices_admin)

    if action == ECS_ACTIONS_ENUM.CREATE.value:
        if len(devices) == 0:
            # ecs_service.create(is_creating_empty_ecs_service=True)
            print("create empty ecs service")
        else:
            # step 1 check  if backend.hcl is exist
            # try:
            #     validate_backend_hcl(file="backend.hcl", path="./terraform")
            #     validate_terraform_tfvars(
            #         file="terraform.tfvars", path="./terraform")
            # except Exception as e:
            #     raise Exception(f"Error validate necessary files : {e}")
            # # check the if backend.hcl is correct

            # # create the dynamodb table lock for terraform
            # create_terraform_dynamondb_lock_table(
            #     dyanmodb_table_name=backend_dyanmodb_table_teraform_state_lock_devices_admin)
            print("=============================")
            print("End of create dynamodb table lock")
            # end of create dynamodb table lock

    if action == ECS_ACTIONS_ENUM.CREATE.value or action == ECS_ACTIONS_ENUM.UPDATE.value:

        print("Create ecs task definition")
        # create the task definition from message body,
        # some of the data are imported from terraform program
        created_task_definiton_name_file_path = create_and_export_task_definition(
            agent_id=agent_id,
            resource_id=resource_id,
            market_interval_in_second=market_interval_in_second,
            devices=devices,
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
            file_name=task_definition_name_file_name,
            path="./terraform/ecs/templates"

        )
        # save task definition file to S3
        s3_service = S3Service(
            bucket_name=BACKEND_S3_BUCKET_NAME,
        )

        s3_service.upload_file(
            source=created_task_definiton_name_file_path,
            destination=f"task_definitions/{agent_id}/{task_definition_name_file_name}"
        )
        print("End of create ecs task definition")
        print("Create ecs service")

        create_terraform_ecs(
            task_definition_file_name=task_definition_name_file_name,
            agent_id=agent_id,
        )

    elif action == ECS_ACTIONS_ENUM.UPDATE.value:
        print("Update")
        # task_definition_name_file_name = f"task-definition-{agent_id}.json.tpl"
        # created_task_definiton_name_file_path = create_and_export_task_definition(
        #     agent_id=agent_id,
        #     resource_id=resource_id,
        #     market_interval_in_second=market_interval_in_second,
        #     devices=devices,
        #     env=ENV,
        #     save_data_url=SAVE_DATA_URL,
        #     get_vens_url=GET_VENS_URL,
        #     participated_vens_url=PARTICIPATED_VENS_URL,
        #     app_image_vtn=APP_IMAGE_VTN,
        #     app_image_ven=APP_IMAGE_VEN,
        #     log_group_name=CLOUDWATCH_NAME,
        #     aws_region=AWS_REGION,
        #     mock_devices_api_url=MOCK_DEVICES_API_URL,
        #     vtn_address=VTN_ADDRESS,
        #     vtn_port=VTN_PORT,
        #     market_prices_url=MARKET_PRICES_URL,
        #     file_name=task_definition_name_file_name,
        #     path="./terraform_ecs/templates"

        # )
        # # save task definition file to S3
        # s3_service = S3Service(
        #     bucket_name=BACKEND_S3_BUCKET_NAME,

        # )

        # s3_service.upload_file(
        #     source=created_task_definiton_name_file_path,
        #     destination=f"task_definitions/{agent_id}/{task_definition_name_file_name}"
        # )
        # # print("task_defition_file ", task_defition_file)
        # # create backend.hcl
        # ecs_service.creagte_backend_hcl_file(
        #     path="./terraform_ecs",
        #     backend_hcl_filename="backend.hcl",
        #     backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
        #     backend_s3_key=f"{PREFIX}-{agent_id}-{ENV}.tfstate",
        #     backend_region=BACKEND_REGION,
        #     backend_dynamodb_table=ECSBackendDynamoDBLockName
        # )
        # # create terraform.auto.tfvars
        # ecs_terraform_auto_tfvars_params = create_ecs_auto_tfvars_params(
        #     task_definition_name_file_name=task_definition_name_file_name,
        #     agent_id=agent_id,
        # )

        # ecs_service.create_terraform_auto_tfvars_file(
        #     path="./terraform_ecs",
        #     terraform_auto_tfvars_file_name="terraform.auto.tfvars",
        #     params=ecs_terraform_auto_tfvars_params
        # )
        # ecs_service.create(is_creating_empty_ecs_service=False)
    if action == ECS_ACTIONS_ENUM.DELETE.value:
        print("DELETE ECS SERVICE")
        s3_service = S3Service(
            bucket_name=BACKEND_S3_BUCKET_NAME,
        )
        # download task definition file
        task_definition_file = s3_service.downlo_file(
        )

        # # create backend.hcl
        # ecs_service.creagte_backend_hcl_file(
        #     path="./terraform_ecs",
        #     backend_hcl_filename="backend.hcl",
        #     backend_s3_bucket=BACKEND_S3_BUCKET_NAME,
        #     backend_s3_key=f"{PREFIX}-{agent_id}-{ENV}.tfstate",
        #     backend_region=BACKEND_REGION,
        #     backend_dynamodb_table=ECSBackendDynamoDBLockName
        # )
        # # create terraform.auto.tfvars
        # ecs_terraform_auto_tfvars_params = create_ecs_auto_tfvars_params(
        #     task_definition_name_file_name=task_definition_name_file_name,
        #     agent_id=agent_id,
        # )

        # task_definition_name_file_path = s3_service.downlo_file(
        #     source=f"task_definitions/{agent_id}/{task_definition_name_file_name}",
        #     destination=f"./terraform_ecs/templates/{task_definition_name_file_name}"
        # )
        # ecs_service.delete()
        return
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
        queue_url=FIFO_SQS_URL)
