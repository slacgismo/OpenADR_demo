from models_and_classes.TerraformExecution import TerraformExecution
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from models_and_classes.Agent import Agent
import os


def create_terraform_dynamondb_lock_table(dyanmodb_table_name: str):
    """
    create dynamodb table for terraform state lock
    params: dyanmodb_table_name: str
    return: None
    """
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
    """
    destroy dynamodb table for terraform state lock
    params: dyanmodb_table_name: str
    return: None

    """
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
    # Todo: check the data
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


def handle_action(action: ECS_ACTIONS_ENUM,
                  message_body: dict,
                  BACKEND_S3_BUCKET_NAME: str,
                  DYNAMODB_AGENTS_TABLE_NAME: str,
                  AWS_REGION: str
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
            print("End of create dynamodb table lock")
            # end of create dynamodb table lock

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
            print("Create ecs task definition")
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
        print("Satet to delete ecs service")
        agent.delete_ecs_service(
            task_definition_file_name=task_definition_file_name,
            backend_s3_state_key=backend_s3_state_key,
            backend_dynamodb_lock_name=backend_dyanmodb_agent_lock_state
        )
        print("Delete the backend dynamodb table lock")
        destroy_terraform_dynamondb_lock_table(
            dyanmodb_table_name=backend_dyanmodb_agent_lock_state
        )
        return
