from models_and_classes.TerraformExecution import TerraformExecution
from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from models_and_classes.DynamoDBService import DynamoDBService, DynamoDB_Key
from models_and_classes.Agent import Agent, AgentState
from models_and_classes.S3Service import S3Service
import json
import os


def add_dynamodb_lock_table_id_to_dynamodb(
        dynamodb_agnets_table_name: str,
        table_id: str,
) -> bool:
    return True


def delete_dynamodb_lock_table_id_to_dynamodb(
        dynamodb_agnets_table_name: str,
        table_id: str,
) -> bool:

    return True


def get_all_dynamodb_lock_table_id_from_dynamodb(
        dynamodb_agnets_table_name: str,
) -> list:
    return []


# def upload_table_list_to_s3(

# )


# def delete_or_update_dynamodb_table_lock_list(
#         s3_bucket_name: str,
#         s3_path: str,
#         file_name: str,
#         is_delete_table: bool,
#         dynamodb_table_name: str,
# ) -> bool:
#     s3_service = S3Service(
#         bucket_name=s3_bucket_name,
#     )
#     table_list_s3_file_path = os.path.join(s3_path, file_name)
#     is_table_list_exist = s3_service.check_file_exists(
#         file_name=table_list_s3_file_path)
#     if is_table_list_exist:
#         # download the file
#         """
#         defualt file name : "dynamodb_table_lock_list.json.tpl"
#         "format : [{"table_name": "table_1"}]
#         """
#         destination = os.path.join("./terraform/templates", file_name)
#         s3_service.download_file(
#             source=table_list_s3_file_path, destination=destination)
#         # read the filt to json object
#         with open(destination, "r") as f:
#             table_list = json.load(f)
#         if not "tables" in table_list:
#             raise Exception(
#                 f"{destination}  is not a valid json file: {table_list}")
#             # check if the table name is exis
#         if is_delete_table:
#             if dynamodb_table_name in table_list['tables']:
#                 table_list['tables'].remove(dynamodb_table_name)
#                 return True

#         if dynamodb_table_name in table_list['tables']:
#             raise Exception(
#                 f"{dynamodb_table_name} is already in the dynamodb table lock list")
#         table_list['tables'].append(dynamodb_table_name)
#         return True
#     else:
#         # create the file that contains the current dynamodb table name
#         if is_delete_table:
#             raise Exception(
#                 f"{dynamodb_table_name} is not in the dynamodb table lock list, you have to create this file first")
#         data = {"tables": ["id1"]}
#         json_data = json.dumps(data)
#         with open(destination, "w") as f:
#             f.write(json_data)
#         return True


def create_terraform_dynamondb_lock_table(
        dynamodb_table_name: str,
        backend_bucket_name: str,
        s3_path: str,
        table_list_json_file_name: str):
    """
    create dynamodb table for terraform state lock
    params: dyanmodb_table_name: str
    return: None
    """
    terrafrom_execution = TerraformExecution(
        working_dir="./terraform",
        name_of_creation="dynamodb",
        environment_variables=(
            {"backend_dyanmodb_table_teraform_state_lock_devices_admin": dynamodb_table_name})
    )
    try:
        # if_creat_or_updated_success = delete_or_update_dynamodb_table_lock_list(
        #     s3_bucket_name=backend_bucket_name,
        #     s3_path=s3_path,
        #     file_name=table_list_json_file_name,
        #     is_delete_table=False,
        #     dynamodb_table_name=dynamodb_table_name
        # )
        # if not if_creat_or_updated_success:
        #     raise Exception("Error updating dynamodb table lock list")
        print("Create or update dynamodb table lock list success")
        print("=============================================")
        print("Start creating dynamodb table ", dynamodb_table_name)

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
        print("=============================================")
        print("Dynamodb table created ", dynamodb_table_name)
        print("=============================================")
        # if sucess then update the dynamodb table lock list
        s3_service = S3Service(
            bucket_name=backend_bucket_name,
        )
        table_list_s3_file_path = os.path.join(path, file_name)

    except Exception as e:
        # apply --auto-approve
        print("Error creating dynamodb table from terraform, destroying the table")
        print("Destroying the table")
        # terrafrom_execution.terraform_destroy()
        raise Exception(f"Error creating dynamodb table from terraform: {e}")


def destroy_terraform_dynamondb_lock_table(
        dynamodb_table_name: str,
        backend_bucket_name: str,
        s3_path: str,
        file_name: str
):
    """
    destroy dynamodb table for terraform state lock
    params: dyanmodb_table_name: str
    return: None

    """
    terrafrom_execution = TerraformExecution(
        working_dir="./terraform",
        name_of_creation="dynamodb",
        environment_variables=(
            {"backend_dyanmodb_table_teraform_state_lock_devices_admin": dynamodb_table_name})
    )
    try:
        # TODO: get all the table id from the dynamodb table lock list

        # s3_service = S3Service(
        #     bucket_name=backend_bucket_name,
        # )
        # table_list_s3_file_path = os.path.join(s3_path, file_name)
        # is_table_list_exist = s3_service.check_file_exists(
        #     file_name=table_list_s3_file_path)
        # if is_table_list_exist:
        #     # download the file
        #     """
        #     defualt file name : "dynamodb_table_lock_list.json.tpl"
        #     "format : [{"table_name": "table_1"}]
        #     """
        #     destination = os.path.join("./terraform/templates", file_name)
        #     s3_service.download_file(
        #         source=table_list_s3_file_path, destination=destination)
        # # init terraform
        # if not os.path.exists(destination):
        #     raise Exception(f"{destination} does not exist")
        terrafrom_execution.terraform_init()
        terrafrom_execution.terraform_destroy()
        print("=============================================")
        print("Dynamodb table destroy ", dynamodb_table_name)
        print("=============================================")
        os.remove(destination)
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
    print("Create task definition file name: ", task_definition_file_name)
    backend_s3_state_key_prefix = f"agent_backend_tfstate"
    backend_s3_state_key = backend_s3_state_key_prefix + f"/{agent_id}-tfstate"
    agent = Agent(
        agent_id=agent_id,
        resource_id=resource_id,
        market_interval_in_second=market_interval_in_second,
        devices=devices,
        backend_s3_bucket_name=BACKEND_S3_BUCKET_NAME,
        s3_bucket_name_of_task_definition_file=BACKEND_S3_BUCKET_NAME,
        DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
        backend_region=AWS_REGION
    )
    if action == ECS_ACTIONS_ENUM.CREATE.value:
        print("=============================================")
        print("Create ecs service", agent_id)
        print("=============================================")
        if len(devices) == 0:
            # ecs_service.create(is_creating_empty_ecs_service=True)
            # TODO: create empty ecs service
            raise Exception(
                "Not support create empty ecs service, if we need to create empty ecs service. Implement it")
        else:

            print("Create ecs task definition")
            try:
                agent.create_ecs_service(
                    task_definition_file_name=task_definition_file_name,
                    backend_s3_state_key=backend_s3_state_key
                )
            except Exception as e:
                # destroy  the dynamodb table just created
                print("Crete the ecs service failed, destroy the dynamodb table lock")

                raise Exception(f"Error create ecs task definition: {e}")
        return
    if action == ECS_ACTIONS_ENUM.UPDATE.value:
        print("=============================================")
        print("Update ecs service", agent_id)
        print("=============================================")

        agent.update_ecs_service(
            task_definition_file_name=task_definition_file_name,
            backend_s3_state_key=backend_s3_state_key,
        )
        return
    if action == ECS_ACTIONS_ENUM.DELETE.value:
        print("=============================================")
        print("Delete ecs service", agent_id)
        print("=============================================")

        print("Satet to delete ecs service")
        agent.delete_ecs_service(
            task_definition_file_name=task_definition_file_name,
            backend_s3_state_key=backend_s3_state_key
        )
        print("Delete the backend dynamodb table lock")
        return
