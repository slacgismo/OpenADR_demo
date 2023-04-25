
import uuid
import json
from decimal import Decimal
import asyncio
# Convert Decimal objects to float
import boto3
from botocore.exceptions import ClientError
from enum import Enum
# from .constants import DynamodbTypes, AttributeTypes, ReturnTypes
import time


class HTTPMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class AttributeTypes(Enum):
    dynamobd_type = 'dynamobd_type'
    return_type = 'return_type'


class DynamodbTypes(Enum):
    string = 'S'
    number = 'N'


class ReturnTypes(Enum):
    string = 'string'
    integer = 'integer'
    float = 'float'
    boolean = 'boolean'


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def get_path(path: str, index: int = 0):

    path_parts = path.split('/')
    if index < len(path_parts):
        return path_parts[index]
    else:
        return None


class TESSError:
    def __init__(self, msg, exception=None):
        self.msg = msg
        self.exception = exception

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


def respond(err=None, res: dict = None, status_code=200):
    response_body = {}
    if err:
        response_body['error'] = err.msg
        if status_code == 200:
            status_code = 400
    else:
        response_body['data'] = res
        # json_data = json.dumps(response_body, default=decimal_default)

    return {
        'statusCode': str(status_code),
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def say_hello():
    return 'Hello world!'


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


async def put_item_to_dynamodb(item: dict,
                               table_name: str,
                               dynamodb_client):
    try:

        response = await asyncio.to_thread(dynamodb_client.put_item,
                                           TableName=table_name,
                                           Item=item
                                           )
        return response

    except Exception as e:
        raise Exception(str(e))


async def get_item_from_dynamodb(id: str, key: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(
            dynamodb_client.get_item,
            TableName=table_name,
            Key={
                key: {DynamodbTypes.string.value: id}
            }
        )
        return response
    except Exception as e:
        raise Exception(str(e))


async def delete_item_from_dynamodb(key: str, id: str, table_name: str, dynamodb_client):

    try:
        response = await asyncio.to_thread(dynamodb_client.delete_item,
                                           TableName=table_name,
                                           Key={
                                               key: {
                                                   DynamodbTypes.string.value: id}
                                           }
                                           )
        return response

    except Exception as e:
        raise Exception(str(e))


def deserializer_dynamodb_data_to_json_format(item: dict, attributesTypes: dict):
    boto3.resource('dynamodb')
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    decimal_data = {k: deserializer.deserialize(
        v) for k, v in item.items()}
    # covert decimal to float
    str_data = json.dumps(
        decimal_data, default=decimal_default)
    json_data = json.loads(str_data)
    # convert the value to correct type
    for key, value in attributesTypes.items():
        return_type = value.get('return_type', None)
        if return_type is None:
            raise TESSError(
                f"  {key}  missing return type {value}")
        if return_type == ReturnTypes.integer.value:
            json_data[key] = int(json_data[key])

    return json_data


def create_item(
        primary_key_name: str,
        primary_key_value: str,
        request_body: dict = None,
        attributeType: dict = None,
        attributes: Enum = None,
):
    item = {}

    valid_at = str(int(time.time()))
    for attribute_name, attribute_info in attributeType.items():
        if attribute_name == attributes.valid_at.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: valid_at
            }
        elif attribute_name == primary_key_name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: primary_key_value
            }
        else:
            value = request_body.get(attribute_name, None)
            if value is None:
                raise TESSError(f"{attribute_name} is missing in request body")
            item[attribute_name] = {
                attribute_info['dynamodb_type']: value
            }
    return item
