"""
This file parse the json data as input and convert to
a task definition of a ECS task.
Then convet to task definition
"""


import json
from typing import List, Dict, Any
import os
from enum import Enum
from .guid import guid
from pathlib import Path


class VTN_TASK_VARIANTS_ENUM(Enum):
    # from fifo sqs message
    ENVIRONMENT = "ENVIRONMENT"
    AGENT_ID = "AGENT_ID"
    RESOURCE_ID = "RESOURCE_ID"
    MARKET_INTERVAL_IN_SECONDS = "MARKET_INTERVAL_IN_SECONDS"
    # from device admin environment variables
    METER_API_URL = "METER_API_URL"
    DEVICES_API_URL = "DEVICES_API_URL"
    ORDERS_API_URL = "ORDERS_API_URL"
    DISPATCHES_API_URL = "DISPATCHES_API_URL"


class VEN_TASK_VARIANTS_ENUM(Enum):
    # from fifo sqs message
    ENVIRONMENT = "ENVIRONMENT"
    AGENT_ID = "AGENT_ID"
    RESOURCE_ID = "RESOURCE_ID"
    METER_ID = "METER_ID"
    DEVICE_ID = "DEVICE_ID"
    DEVICE_TYPE = "DEVICE_TYPE"
    DEVICE_SETTINGS = "DEVICE_SETTINGS"
    MARKET_INTERVAL_IN_SECONDS = "MARKET_INTERVAL_IN_SECONDS"
    FLEXIBLE = "FLEXIBLE"
    # from device admin environment variables
    EMULATED_DEVICE_API_URL = "EMULATED_DEVICE_API_URL"
    IS_USING_MOCK_DEVICE = "IS_USING_MOCK_DEVICE"


CONTAINER_DEFINITION_TEMPLATE = ({
    "name": "vtn",
    "image": "${app_image_vtn}",
    "essential": True,
    "memoryReservation": 256,
    "runtimePlatform": {
        "operatingSystemFamily": "LINUX",
        "cpuArchitecture": "ARM64"
    },
    "entryPoint": ["sh", "-c"],
    "command": ["python vtn.py"],

})


def create_ven_params(
    env: str,
    device_id: str,
    resource_id: str,
    meter_id: str,
    agent_id: str,
    EMULATED_DEVICE_API_URL: str,
    device_type: str,
    device_settings: dict,
    market_interval_in_seconds: str,
    flexible: str,
    is_using_mock_device: bool,
) -> dict:
    ven_params = dict()
    for ven_task in VEN_TASK_VARIANTS_ENUM:
        key = ven_task.value
        if key == VEN_TASK_VARIANTS_ENUM.ENVIRONMENT.value:
            ven_params[key] = env
        elif key == VEN_TASK_VARIANTS_ENUM.DEVICE_ID.value:
            ven_params[key] = device_id
        elif key == VEN_TASK_VARIANTS_ENUM.RESOURCE_ID.value:
            ven_params[key] = resource_id
        elif key == VEN_TASK_VARIANTS_ENUM.METER_ID.value:
            ven_params[key] = meter_id
        elif key == VEN_TASK_VARIANTS_ENUM.AGENT_ID.value:
            ven_params[key] = agent_id
        elif key == VEN_TASK_VARIANTS_ENUM.DEVICE_TYPE.value:
            ven_params[key] = device_type
        elif key == VEN_TASK_VARIANTS_ENUM.EMULATED_DEVICE_API_URL.value:
            ven_params[key] = EMULATED_DEVICE_API_URL
        elif key == VEN_TASK_VARIANTS_ENUM.DEVICE_SETTINGS.value:
            ven_params[key] = device_settings
        elif key == VEN_TASK_VARIANTS_ENUM.MARKET_INTERVAL_IN_SECONDS.value:
            ven_params[key] = market_interval_in_seconds
        elif key == VEN_TASK_VARIANTS_ENUM.FLEXIBLE.value:
            ven_params[key] = flexible
        elif key == VEN_TASK_VARIANTS_ENUM.IS_USING_MOCK_DEVICE.value:
            ven_params[key] = is_using_mock_device
        else:
            raise Exception(
                f"ven key {key} is not set, please check your code")

    return ven_params


def create_vtn_params(
    market_interval_in_seconds: str,
    agent_id: str,
    resource_id: str,
    env: str,
    METER_API_URL: str,
    DEVICES_API_URL: str,
    ORDERS_API_URL: str,
    DISPATCHES_API_URL: str,
) -> dict:
    vtn_params = dict()
    # for key, value in enumerate(VTN_TASK_VARIANTS_ENUM):
    for vtn_task in VTN_TASK_VARIANTS_ENUM:
        key = vtn_task.value
        if key == VTN_TASK_VARIANTS_ENUM.METER_API_URL.value:
            vtn_params[key] = METER_API_URL
        elif key == VTN_TASK_VARIANTS_ENUM.DEVICES_API_URL.value:
            vtn_params[key] = DEVICES_API_URL
        elif key == VTN_TASK_VARIANTS_ENUM.ORDERS_API_URL.value:
            vtn_params[key] = ORDERS_API_URL
        elif key == VTN_TASK_VARIANTS_ENUM.DISPATCHES_API_URL.value:
            vtn_params[key] = DISPATCHES_API_URL
        elif key == VTN_TASK_VARIANTS_ENUM.MARKET_INTERVAL_IN_SECONDS.value:
            vtn_params[key] = market_interval_in_seconds
        elif key == VTN_TASK_VARIANTS_ENUM.AGENT_ID.value:
            vtn_params[key] = agent_id
        elif key == VTN_TASK_VARIANTS_ENUM.RESOURCE_ID.value:
            vtn_params[key] = resource_id
        elif key == VTN_TASK_VARIANTS_ENUM.ENVIRONMENT.value:
            vtn_params[key] = env
        else:
            raise Exception(
                f"vtn key {key} is not set, please check your code")
    return vtn_params


def export_to_json_tpl(data, filename):
    """
    Export data to json file
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def generate_vtn_task_definition(
    vtn_template: dict,
    vtn_id: str,
    agent_id: str,
    app_image_vtn: str,
    log_group_name: str,
    log_group_region: str,
    environment_variables: dict,
    vtn_address: str,
    vtn_port: str,
) -> dict:
    """

    """
    vtn_template['name'] = vtn_id
    vtn_template['image'] = app_image_vtn
    vtn_template['environment'] = [{"name": key.upper(), "value": value}
                                   for key, value in environment_variables.items()]

    vtn_template['portMappings'] = [
        {
            "containerPort": 8080,
            "hostPort": 8080
        }
    ]
    vtn_template['mountPoints'] = [
        {
            "readOnly": False,
            "containerPath": f"/vol/{vtn_id}",
            "sourceVolume": "agent-volume"
        }
    ]

    vtn_template['healthCheck'] = {
        "retries": 3,
        "command": [
            "CMD-SHELL",
            f"curl -f http://{vtn_address}:{vtn_port}/health || exit 1"

        ],
        "timeout": 5,
        "interval": 30
    }

    vtn_template['logConfiguration'] = {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": log_group_name,
            "awslogs-region": log_group_region,
            "awslogs-stream-prefix": f"{agent_id}-{vtn_id}"
        }
    }
    return vtn_template


def generate_ven_task_definition(
    ven_template: dict,
    ven_id: str,
    agent_id: str,
    app_image_ven: str,
    log_group_name: str,
    log_group_region: str,
    environment_variables: dict

) -> dict:
    """
    environment_variables:[
        "env": "str",
        "ven_id": "str"
        "meter_id": "str"
        "agent_id": "str",
        "device_id": "str",
        "device_name":"str",
        "device_type": str,
        "vtn_address": str,
        "vtn_port": str,
        "mock_devices_api_url": str,
        "device_settings": dict,
        "market_interval_in_seconds": str,
        "price_threshold": str
    ]


    """
    ven_id = ven_id
    ven_template['name'] = ven_id
    ven_template['image'] = app_image_ven
    ven_template['command'] = ["python ven.py"]
    ven_template['environment'] = [{"name": key.upper(), "value": value}
                                   for key, value in environment_variables.items()]

    ven_template['mountPoints'] = [
        {
            "readOnly": False,
            "containerPath": f"/vol/{ven_id}",
            "sourceVolume": "agent-volume"
        }
    ]
    ven_template['mountPoints'] = [
        {
            "readOnly": False,
            "containerPath": f"/vol/{ven_id}",
            "sourceVolume": "agent-volume"
        }
    ]
    # ven_template['healthCheck'] = {
    #     "retries": 3,
    #     "command": [
    #         "CMD-SHELL",
    #         f"curl -f http://localhost:8000/health || exit 1"

    #     ],
    #     "timeout": 5,
    #     "interval": 30
    # }
    ven_template['logConfiguration'] = {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": log_group_name,
            "awslogs-region": log_group_region,
            "awslogs-stream-prefix": f"{agent_id}-{ven_id}"
        }
    }
    return ven_template


def combine_vtn_and_vens_as_task_definition(
        vtn_definition: dict,
        vens_definition: list,
) -> dict:
    """

    """
    task_definition = list()
    task_definition.append(vtn_definition)
    for ven_definition in vens_definition:
        task_definition.append(ven_definition)

    return task_definition


def export_task_definition_to_tpl(
        task_definition: str,
        file_name: str):
    """
    Export task definition to local file
    """
    definition_file_name = file_name
    export_to_json_tpl(
        task_definition, definition_file_name)

    return True


def parse_message_body_to_vtn_environment_variables(
        message_body: dict,
) -> dict:
    """
    params: message_body: dict
    """
    variables = dict()
    agent_id = message_body['agent_id']
    resource_id = message_body['resource_id']

    return variables


def create_and_export_task_definition(
    agent_id: str,
    market_interval_in_seconds: str,
    resource_id: str,
    env: str,
    METER_API_URL: str,
    DEVICES_API_URL: str,
    ORDERS_API_URL: str,
    DISPATCHES_API_URL: str,
    devices: list,
    app_image_vtn: str,
    log_group_name: str,
    aws_region: str,
    vtn_address: str,
    vtn_port: str,
    app_image_ven: str,
    EMULATED_DEVICE_API_URL: str,
    file_name: str,
    path: str,

) -> bool:
    """
    parse message body and create task definition
    params: message_body: dict
    params: file_name:
    params: path:
    """
    if not os.path.exists(path):
        raise Exception(f"{path} path not found")
    vtn_id = 'vtn-' + agent_id

    vtn_environment_variables = create_vtn_params(
        market_interval_in_seconds=market_interval_in_seconds,
        agent_id=agent_id,
        resource_id=resource_id,
        env=env,
        METER_API_URL=METER_API_URL,
        DEVICES_API_URL=DEVICES_API_URL,
        ORDERS_API_URL=ORDERS_API_URL,
        DISPATCHES_API_URL=DISPATCHES_API_URL,
    )

    vtn_container_definition = generate_vtn_task_definition(
        vtn_template=CONTAINER_DEFINITION_TEMPLATE.copy(),
        vtn_id=vtn_id,
        agent_id=agent_id,
        app_image_vtn=app_image_vtn,
        log_group_name=log_group_name,
        log_group_region=aws_region,
        environment_variables=vtn_environment_variables,
        vtn_address=vtn_address,
        vtn_port=vtn_port,
    )
    # if "devices" not in message_body:
    #     raise Exception("devices not found in message body")
    # devices = message_body['devices']
    ven_container_definition_list = list()
    vens_info = list()

    for device in devices:

        device_id = device['device_id']
        meter_id = device['meter_id']
        device_type = device['device_type']
        flexible = device['flexible']
        is_using_mock_device = device['is_using_mock_device']

        ven_environment_variables = dict()
        for key, value in enumerate(VEN_TASK_VARIANTS_ENUM):

            # have convet json format to string to pass to ven
            device_settings_str = json.dumps(device["device_settings"])

            ven_environment_variables = create_ven_params(
                env=env,
                resource_id=resource_id,
                meter_id=meter_id,
                device_id=device_id,
                agent_id=agent_id,
                EMULATED_DEVICE_API_URL=EMULATED_DEVICE_API_URL,
                device_type=device_type,
                device_settings=device_settings_str,
                market_interval_in_seconds=market_interval_in_seconds,
                flexible=str(flexible),
                is_using_mock_device=str(is_using_mock_device),
            )
        ven_id = 'ven-' + device_id
        vens_info.append({
            "ven_id": ven_id,
            "device_id": device_id,
            "meter_id": meter_id
        })
        ven_container_definition = generate_ven_task_definition(
            ven_template=CONTAINER_DEFINITION_TEMPLATE.copy(),
            ven_id=ven_id,
            agent_id=agent_id,
            app_image_ven=app_image_ven,
            log_group_name=log_group_name,
            log_group_region=aws_region,
            environment_variables=ven_environment_variables,
        )

        ven_container_definition_list.append(ven_container_definition)
    # combine vtn and ven definition
    task_definition = combine_vtn_and_vens_as_task_definition(
        vtn_definition=vtn_container_definition,
        vens_definition=ven_container_definition_list
    )
    # print("task_definition: ", task_definition)
    # export to file
    path_file_name = os.path.join(path, file_name)
    export_to_json_tpl(task_definition, path_file_name)
    return path_file_name, vtn_id, vens_info
