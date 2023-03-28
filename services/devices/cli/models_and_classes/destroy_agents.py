from .ECSService import ECSService
from .SQSService import SQSService
from .create_agents import create_messages_list
from .ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
from .S3Service import S3Service
import re
import time
import os
import logging
import json
from typing import Tuple


def extract_first_and_second_word(text):
    pattern = r'^[^-]+-([^-\s]+)-([^-\s]+)'
    match = re.search(pattern, text)
    if match:
        first_word = match.group(1)
        second_word = match.group(2)
        return first_word, second_word
    return None, None


def destroy_all(
    ecs_cluster_name: str = None,
    fifo_sqs: str = None,
    group_id: str = None
):
    # list number of workers
    ecs_service = ECSService(
        ecs_cluster_name=ecs_cluster_name
    )
    active_agents_list = ecs_service.list_ecs_services()
    # find agenet id
    # download task definition from s3
    if active_agents_list is None:
        return
    agent_ids = []
    for agent in active_agents_list:
        app, id = extract_first_and_second_word(agent)
        if app == "agent":
            agent_ids.append(id)

    command_list = list()
    for agent_id in agent_ids:
        logging.info(f"Find agent id:  {agent_id}")
        body = {

            "agent_id": agent_id,
            "resource_id": "",
            "market_interval_in_second": "",
            "market_id": "",
            "devices": [
                {
                    "device_id": "",
                    "device_name": "",
                    "device_type": "",
                    "device_params": {
                        "battery_token": "",
                        "battery_sn": "",
                        "device_brand": ""
                    },
                    "biding_price_threshold": "",
                    "meter_id": "",
                }
            ]
        }
        # os.remove(destination)
        command_list.append(body)
    messages = create_messages_list(
        command_list=command_list,
        MessageGroupId=group_id,
        ecs_action=ECS_ACTIONS_ENUM.DELETE.value,

    )
    logging.info(f"number of agents:  {len(command_list)}")
    sqs_service = SQSService(
        queue_url=fifo_sqs
    )
    for message in messages:
        sqs_service.send_message(
            message_body=message['MessageBody'],
            message_attributes=message['MessageAttributes'],
            message_group_id=message['MessageGroupId']
        )
        logging.info(f"Send out message {message['MessageBody']}")
        time.sleep(2)
    return


# def parse_task_definition(task_definition_file):
#     """
#     {
#     "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
#     "resource_id": "caff6719c24359a155a4d0d2f265a7",
#     "market_interval_in_second": "300",
#     "market_id": "6436a67e184d3694a15886215ae464",
#     "devices": [
#         {
#             "device_id": "807f8e4a37446e80c5756a74a3598d",
#             "device_name": "battery_0",
#             "device_type": "ES",
#             "device_params": {
#                 "battery_token": "12321321qsd",
#                 "battery_sn": "66354",
#                 "device_brand": "SONNEN_BATTERY"
#             },
#             "biding_price_threshold": "0.15",
#             "meter_id": "6436a67e184d3694a15886215ae464"
#         }
#     ]
#     }
#     """
#     if not os.path.exists(task_definition_file):
#         raise Exception(f"File {task_definition_file} does not exist")
#     task_params = {}
#     try:
#         with open(task_definition_file, "r") as f:
#             task_params = json.load(f)
#             print(task_params)
#             # agent_id = task_params.get("agent_id")
#             # resource_id = task_params.get("resource_id")
#             # market_interval_in_second = task_params.get(
#             #     "market_interval_in_second")
#             # market_id = task_params.get("market_id")
#             # devices = task_params.get("devices")
#             # return agent_id, resource_id, market_interval_in_second, market_id, devices
#     except Exception as e:
#         raise Exception(
#             f"Error when parsing task definition file {e}")
