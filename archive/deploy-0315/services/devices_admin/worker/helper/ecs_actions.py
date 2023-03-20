
from .task_definition_generator import create_and_export_task_definition


# def create_empty_ecs_services(agent_id):
#     print("No devices in the message, create empty ecs services")
#     return


def create_ecs_service(message_body,
                       vtn_env_params: dict,
                       ven_env_params: dict,
                       log_group_name: str,
                       aws_region: str,
                       app_image_ven: str,
                       app_image_vtn: str,
                       tags: dict
                       ):
    print("create_ecs")
    # check if agent_id is in the message
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
    devices = message_body["devices"]
    market_interval_in_second = message_body["market_interval_in_second"]
    agent_id = message_body['agent_id']
    agent_definition = []
    # check if device_ids is in the message
    if len(devices) == 0:
        print("No devices in the message, create empty ecs services")
        create_ecs_service_with_no_task()
        return
    # create ecs_service with vtn, vens
    print("create task definition contain a vtn and vens")
    # conver message_body and environment variable to to vtn_task_definition_params and ven_task_definition_params

    task_definition_file = create_and_export_task_definition(
        message_body=message_body,
        vtn_task_definition_params=vtn_task_definition_params,
        ven_task_definition_params=ven_task_definition_params,
        log_group_name=log_group_name,
        aws_region=aws_region,
        vtn_address=vtn_address,
        vtn_port=vtn_port,
        app_image_vtn=app_image_vtn,
        app_image_ven=app_image_ven,
        file_name=f"task_definition-{agent_id}.json.tpl",
        path="./task_definition"
    )

    return None


def read_ecs(message_body):
    print("read_ecs")
    return None


def update_ecs(message_body):
    print("update_ecs")
    return None


def delete_ecs(message_body):
    print("Delete_ecs")
    return None
