import os
import boto3
import json
import time
from datetime import datetime
from enum import Enum
import uuid
try:
    from_event_queue_url = os.environ['FROM_EVENT_QUEUE_URL']
    to_trigger_queue_url = os.environ['TO_TRIGGER_QUEUE_URL']
    meters_table = os.environ['METERS_TABLE']
    market_table = os.environ['MARKETS_TABLE']
    agent_table = os.environ['AGENTS_TABLE']
    settings_table = os.environ['SETTINGS_TABLE']
    # os.environ['METERS_TABLE_GLOBAL_INDEX']
    meters_table_global_index = "resource-device-index"
    markets_table_global_index = "resource_id-index"
    settings_table_global_index = "device_id-index"
except Exception as e:
    print(f"Error getting environment variables: {e}")
    raise e

sqs = boto3.client('sqs')
'''
{'body': '{"eventID": "60edf1b1d52db87046e6ec8ca4c72f2f", "eventName": "MODIFY", "eventVersion": "1.1", "eventSource": "aws:dynamodb", "awsRegion": "us-east-2", "dynamodb": {"ApproximateCreationDateTime": 1681414497.0, "Keys": {"device_id": {"S": "37a6d01bf4009ae512d640ac594856d3"}}, "NewImage": {"agent_id": {"S": "2312"}, "device_id": {"S": "37a6d01bf4009ae512d640ac594856d3"}, "device_type": {"S": "ES"}, "valid_at": {"N": "1681414496"}}, "SequenceNumber": "7220700000000021559578469", "SizeBytes": 121, "StreamViewType": "NEW_IMAGE"}, "eventSourceARN": "arn:aws:dynamodb:us-east-2:041414866712:table/openadr-NHEC-dev-devices/stream/2023-04-12T06:46:05.602"}',
    'attributes': {'ApproximateReceiveCount': '1', 'AWSTraceHeader': 'Root=1-64385961-093b32c83faa42ef919c7c67;Parent=00e2cff84f1d3678;Sampled=0;Lineage=70eb5c3b:0', 'SentTimestamp': '1681414498103', 'SenderId': 'AROAQTJEEW4MMPJ2OY5Y3:openadr-NHEC-dev-lambda-dynamodb-event-trigger', 'ApproximateFirstReceiveTimestamp': '1681414498104'}, 'messageAttributes': {}, 'md5OfBody': '85db669ef954ebcc5c56dc6fb14942fe', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-2:041414866712:openadr-NHEC-dev-devices-sqs', 'awsRegion': 'us-east-2'}
'''


class EventName (Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


class DevicesTableAttribute (Enum):
    DEVICE_ID = "device_id"
    AGENT_ID = "agent_id"
    DEVICE_TYPE = "device_type"
    VALID_AT = "valid_at"


class AgentsTableAttribute (Enum):
    AGENT_ID = "agent_id"
    RESOURCE_ID = "resource_id"
    VALID_AT = "valid_at"


class MetersTableAttribute (Enum):
    METER_ID = "meter_id"
    DEVICE_ID = "device_id"
    RESOURCE_ID = "resource_id"
    STATUS = "status"
    VALID_AT = "valid_at"


class MarketsTableAttribute (Enum):
    MARKET_ID = "market_id"
    NAME = "name"
    RESOURCE_ID = "resource_id"
    UNITS = "units"
    PRICE_FLOOR = "price_floor"
    PRICE_CEILING = "price_ceiling"
    INTERVAL = "interval"
    VALID_AT = "valid_at"

# NEED TO CHECK WITH JOHN ABOUT THIS
# class SETTINGS_TABLE_ATTRIBUTE (Enum):
#     SETTING_ID = "setting_id"
#     DEVICE_ID = "device_id"
#     NAME = "name"
#     VALUE = "value"
#     VALID_AT = "valid_at"


def handler(event, context):
    print(f"triggered by SQS :{event}")
    if event:
        batch_item_failures = []
        sqs_batch_response = {}

        for record in event["Records"]:
            try:

                # process message
                message_body = json.loads(record['body'])
                print("message_body: ", message_body)
                # Do something with the message body...
                if 'eventName' not in message_body:
                    raise Exception("eventName is missing from message body")

                eventName = message_body['eventName']
                print("eventName: ", eventName)
                handle_event(event_name=eventName, body=message_body,
                             to_trigger_queue_url=to_trigger_queue_url)
                # Delete the message
                response = sqs.delete_message(
                    QueueUrl=from_event_queue_url,
                    ReceiptHandle=record['receiptHandle']
                )
                print(f"Deleted message {record['messageId']}: {response}")

            except Exception as e:
                batch_item_failures.append(
                    {"itemIdentifier": record['messageId']})

        sqs_batch_response["batchItemFailures"] = batch_item_failures
        return sqs_batch_response


def handle_event(event_name: EventName, body: dict, to_trigger_queue_url: str = None):
    # parse new image
    print("Handling event: ", event_name)
    if 'dynamodb'not in body:
        raise Exception("dynamodb is missing from message body")

    if event_name == EventName.INSERT.value:
        new_image = body['dynamodb']['NewImage']

        if 'device_id' not in new_image or 'agent_id' not in new_image or 'device_type' not in new_image:
            raise Exception(
                "device_id, device_type or agent_id is missing from message body")
        device_id = new_image['device_id']['S']
        agent_id = new_image['agent_id']['S']
        device_type = new_image['device_type']['S']

        sq_message = create_sqs_message(
            device_id=device_id, agent_id=agent_id, eventName=event_name, device_type=device_type)
        response = send_message_to_sqs(
            message=sq_message, queue_url=to_trigger_queue_url)
        print(f"sqs response: {response}")

    elif event_name == EventName.REMOVE.value:
        print("Handling remove: ========================")
        if 'OldImage' not in body['dynamodb']:
            raise Exception("OldImage is missing from message body")

        old_image = body['dynamodb']['OldImage']
        old_device_id = old_image[DevicesTableAttribute.DEVICE_ID.value]['S']
        old_agent_id = old_image[DevicesTableAttribute.AGENT_ID.value]['S']
        old_device_type = old_image[DevicesTableAttribute.DEVICE_TYPE.value]['S']
        remove_message = create_sqs_message(
            device_id=old_device_id, agent_id=old_agent_id, eventName=EventName.REMOVE.value, device_type=old_device_type)
        remove_response = send_message_to_sqs(
            message=remove_message, queue_url=to_trigger_queue_url)
        print(f"sqs remove_response: {remove_response}")
    elif event_name == EventName.MODIFY.value:
        # break into remove and insert
        # first check if agent_id is changed or device_type is changed
        # if none of them is changed, do nothing
        # if agent_id or device_type is changed, send remove message to trigger queue

        if 'OldImage' not in body['dynamodb']:
            raise Exception("OldImage is missing from message body")

        if 'NewImage' not in body['dynamodb']:
            raise Exception("NewImage is missing from message body")
        old_image = body['dynamodb']['OldImage']
        old_device_id = old_image[DevicesTableAttribute.DEVICE_ID.value]['S']
        old_agent_id = old_image[DevicesTableAttribute.AGENT_ID.value]['S']
        old_device_type = old_image[DevicesTableAttribute.DEVICE_TYPE.value]['S']

        new_image = body['dynamodb']['NewImage']
        new_device_id = new_image[DevicesTableAttribute.DEVICE_ID.value]['S']
        new_agent_id = new_image[DevicesTableAttribute.AGENT_ID.value]['S']
        new_device_type = new_image[DevicesTableAttribute.DEVICE_TYPE.value]['S']
        if old_agent_id == new_agent_id and old_device_type == new_device_type:
            print("agenit_id and device_type are the same, do nothing")
            return
        else:
            # remove the old
            remove_message = create_sqs_message(
                device_id=old_device_id, agent_id=old_agent_id, eventName=EventName.REMOVE.value, device_type=old_device_type)
            remove_response = send_message_to_sqs(
                message=remove_message, queue_url=to_trigger_queue_url)
            print(f"remove response: {remove_response}")
            insert_message = create_sqs_message(
                device_id=new_device_id, agent_id=new_agent_id, eventName=EventName.INSERT.value, device_type=new_device_type)
            insert_response = send_message_to_sqs(
                message=insert_message, queue_url=to_trigger_queue_url)

            print(f"insert response: {insert_response}")
            return

    else:
        raise Exception("Invalid event name")


def create_sqs_message(device_id: str, agent_id: str, eventName: EventName, device_type: str):
    """
    {
        "eventName": "INSERT",
        "agent_id": "00ccff430c4bcfa1f1186f488b88fc",
        "resource_id": "caff6719c24359a155a4d0d2f265a7",
        "market_interval_in_seconds": "300",
        "device_id": "807f8e4a37446e80c5756a74a3598d",
        "device_type": "ES",
        "meter_id": "6436a67e184d3694a15886215ae464"
        "price_floor": 0,
        "price_ceiling": 100,
        "device_settings": {
            "battery_token": "12321321qsd",
            "battery_sn": "66354",
            "device_brand": "SONNEN_BATTERY"
            "is_using_mock_device": true
            "flexible": "1",
        }

    }
    """
    # get meter_id from meter table with device_id and resource_id
    dynamodb_client = boto3.client('dynamodb')
    meters_table_global_index_value = device_id + resource_id
    meter_item = get_item_from_table(
        table_name=meters_table, key=meters_table_global_index, value=meters_table_global_index_value, dynamodb_client=dynamodb_client)

    meter_id = meter_item[MetersTableAttribute.METER_ID.value]['S']
    print("meter_item: ", meter_item)
    # get resource id from agent table with agent_id
    agent_item = get_item_from_table(
        table_name=agent_table, key=AgentsTableAttribute.AGENT_ID.value, value=agent_id, dynamodb_client=dynamodb_client)

    print("agent item: ", agent_item)
    resource_id = agent_item[AgentsTableAttribute.RESOURCE_ID.value]['S']

    # resource_id = "caff6719c24359a155a4d0d2f265a7"
    # get market interval from market table with resource_id
    market_item = get_item_from_table(
        table_name=market_table, key=markets_table_global_index, value=resource_id, dynamodb_client=dynamodb_client)
    print("market item: ", market_item)
    market_interval_in_seconds = market_item[MarketsTableAttribute.INTERVAL.value]['N']
    price_floor = market_item[MarketsTableAttribute.PRICE_FLOOR.value]['N']
    price_ceiling = market_item[MarketsTableAttribute.PRICE_CEILING.value]['N']

    # market_interval_in_seconds = "60"
    settings_item = get_item_from_table(
        table_name=settings_table, key="device_id", value=settings_table_global_index, dynamodb_client=dynamodb_client)
    # get device flexible  from setting table
    print("settings item: ", settings_item)
    flexible = settings_item['flexible']['S']
    battery_token = settings_item['battery_token']['S']
    battery_sn = settings_item['battery_sn']['S']
    device_brand = settings_item['device_brand']['S']
    is_using_mock_device = settings_item['is_using_mock_device']['S']

    # battery_token = "12321321qsd"
    # battery_sn = "66354"
    # device_brand = "SONNEN_BATTERY"
    # is_using_mock_device = "true"
    # flexible = "1"

    message = {
        "eventName": eventName,
        "agent_id": agent_id,
        "resource_id": resource_id,
        "market_interval_in_seconds": market_interval_in_seconds,
        "device_id": device_id,
        "device_type": device_type,
        "meter_id": meter_id,
        "price_floor": price_floor,
        "price_ceiling": price_ceiling,
        "device_settings": {
            "battery_token": battery_token,
            "battery_sn": battery_sn,
            "device_brand": device_brand,
            "is_using_mock_device": is_using_mock_device,
            "flexible": flexible
        }
    }
    print("Message created: ", message)
    return message


def send_message_to_sqs(message: dict, queue_url: str):
    sqs = boto3.client('sqs')
    print(f"Send to {queue_url}")
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageGroupId='AWS',
            MessageDeduplicationId=str(guid()),
            MessageBody=json.dumps(message)
        )
        print(f"Message sent to SQS: {response}")
    except Exception as e:
        print(f"Error sending message to SQS: {e}")
        raise e


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


def get_item_from_table(table_name: str, key: str, value: str, dynamodb_client) -> dict:
    try:
        table = dynamodb_client.Table(table_name)
        response = table.get_item(
            Key={
                key: value
            }
        )
        print(f"response: {response}")
        return response
    except Exception as e:
        print(f"Error getting item from table: {e}")
        raise e
