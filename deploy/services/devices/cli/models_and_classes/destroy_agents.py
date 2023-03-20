from .ECSService import ECSService
from .SQSService import SQSService
from .create_agents import create_messages_list
from .ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
import re
import time


def destroy_all(
    ecs_cluster_name: str = None,
    fifo_sqs: str = None
):
    # list number of workers
    esc_service = ECSService(
        ecs_cluster_name=ecs_cluster_name
    )
    active_agents_list = esc_service.list_ecs_service()
    # find agenet id
    # download task definition from s3

    agent_ids = []
    for agent in active_agents_list:
        pattern = r'-(.*)'
        match = re.search(pattern, agent)
        if match:
            agent_id = match.group(1)
            agent_ids.append(agent_id)
    # TODO: download task definition from s3
    # TODO: parse task definition to get the resource id, market interval, devices
    # TODO: create sqs message
    # TODO: send sqs message

    # sqs_messages = create_messages_list(
    #     command_list=command_list,
    #     ecs_action=ECS_ACTIONS_ENUM.DELETE.value,
    #     MessageGroupId="test"
    # )
    # print("destroy workers", ECSService)
    # sqs_service = SQSService(
    #     queue_url=fifo_sqs,

    # )
    # for message in sqs_messages:
    #     sqs_service.send_message(
    #         message_body=message['MessageBody'],
    #         message_attributes=message['MessageAttributes'],
    #         message_group_id=message['MessageGroupId']
    #     )
    #     time.sleep(1)

    # print(f"Send out {len(sqs_messages)} sqs messages")
    return
