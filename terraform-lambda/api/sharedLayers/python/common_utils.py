
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


def conver_josn_to_dynamodb_format(
        hash_key: str = None,
        timestam_index_name: str = 'valid_at',
        items: list = None,
        attributesType: dict = None) -> dict:
    """
    Convet json to dynamodb format
    Create a unique id for each hash key
    Create a valid_at current timestamp
    params: hash_key: hash key
    params: items: list of items
    params: attributesType: dictionary of attributes and type
    return: dynamodb_items: list of dynamodb items
    return: created_hash_keys: list of created hash keys
    """
    dynamodb_items = []
    created_hash_keys = []
    for item in items:
        dynamodb_item = {}
        for key, value in attributesType.items():
            # print(key, value['dynamodb_type'])
            dynamodb_type = value['dynamodb_type']
            # valid at is the current timestamp
            if key == timestam_index_name:
                item_value = str(int(time.time()))
            # create a unique id for hash key
            elif key == hash_key:
                item_value = str(guid())
                hash_key_item = {hash_key: item_value}
                created_hash_keys.append(hash_key_item)
            else:
                item_value = item[key]
            dynamodb_item[key] = {dynamodb_type: item_value}

        dynamodb_items.append(dynamodb_item)
    # print(dynamodb_items)
    return dynamodb_items, created_hash_keys


async def delete_batch_items_from_dynamodb(chunks: list = None, key_type: str = 'S',  table_name: str = None, dynamodb_client: boto3.client = None, page_size: int = 25):
    """
    params: chunks: list of items
            example : [{'agent_id':'ccfd65441d4874921dd765eb0dc455'}]
    params: table_name: dynamodb table name
    params: dynamodb_client: boto3 client
    params: page_size: number of items per page
    """
    try:
        items = []
        # convert list of dictionary to dynamodb format
        for chunk in chunks:
            # Convert dictionary to DynamoDB format
            # Example: {'agent_id': {'S': 'ccfd65441d4874921dd765eb0dc455'}}
            item = {}
            for key, value in chunk.items():
                item[key] = {key_type: value}
            items.append({'DeleteRequest': {'Key': item}})

        # Use pagination to delete items in batches
        last_evaluated_key = None
        while True:
            # Set the pagination parameters
            pagination_params = {
                'TableName': table_name,
                'Key': items,
                'ReturnConsumedCapacity': 'TOTAL',
                'Limit': page_size,
            }
            if last_evaluated_key:
                pagination_params['ExclusiveStartKey'] = last_evaluated_key

            # Delete items in the current page
            response = await asyncio.to_thread(dynamodb_client.batch_write_item,
                                               RequestItems={table_name: items})

            # Check if there are more pages to delete
            if 'UnprocessedItems' in response and response['UnprocessedItems']:
                items = response['UnprocessedItems'][table_name]
                last_evaluated_key = response.get('LastEvaluatedKey')
            else:
                break

        return True
    except Exception as e:
        raise Exception(str(e))


async def query_items_from_dynamodb(
        table_name: str = None,
        gsi_name: str = None,
        gsi_value: str = None,
        hash_key: str = None,
        hash_key_type: str = 'S',
        dynamodb_client: boto3.client = None,
        page_size: int = 25,
        range_key: str = None,
        range_key_type: str = 'N',
        start_from: str = 0,
        end_at: str = None):
    try:
        items = []
        last_evaluated_key = None
        while True:
            # Set the pagination parameters
            key_condition_expression = f"{hash_key} = :{hash_key}"
            expression_attribute_values = {
                f':{hash_key}': {hash_key_type: gsi_value}}
            if range_key is not None:
                key_condition_expression += ' AND {} BETWEEN :start_from AND :end_at'.format(
                    range_key)
                expression_attribute_values[':start_from'] = {
                    range_key_type: str(start_from)}
                expression_attribute_values[':end_at'] = {
                    range_key_type: str(end_at)}

            pagination_params = {
                'TableName': table_name,
                'IndexName': gsi_name,
                'KeyConditionExpression': key_condition_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnConsumedCapacity': 'TOTAL',
                'Limit': page_size,
            }
            if last_evaluated_key:
                pagination_params['ExclusiveStartKey'] = last_evaluated_key

            # Query items in the current page
            response = await asyncio.to_thread(dynamodb_client.query, **pagination_params)
            print(response)
            print("-----------------")
            # Add the items to the list
            for item in response.get('Items', []):
                # Convert DynamoDB format to dictionary
                # Example: {'agent_id': {'S': 'ccfd65441d4874921dd765eb0dc455'}}
                item_dict = {}
                for key, value in item.items():
                    item_dict[key] = value.get('S', value.get('N'))
                items.append(item_dict)

            # Check if there are more pages to query
            if 'LastEvaluatedKey' in response and response['LastEvaluatedKey']:
                last_evaluated_key = response['LastEvaluatedKey']
            else:
                break

        print(items)
        return items
    except Exception as e:
        raise Exception(str(e))


async def write_batch_items_to_dynamodb(chunks: list = None, table_name: str = None, dynamodb_client: boto3.client = None, page_size: int = 25):
    """
    params: chunks: list of items
            example: {'agent_id': {'S': '12321'}, 'resource_id': {
                'S': '1'}, 'status': {'N': '1'}, 'valid_at': {'N': '1682444347'}}
    params: table_name: dynamodb table name
    params: dynamodb_client: boto3 client
    params: page_size: number of items per page

    """
    try:
        items = []
        for chunk in chunks:

            items.append({'PutRequest': {'Item': chunk}})

        # Use pagination to write items in batches
        last_evaluated_key = None
        while True:
            # Set the pagination parameters
            pagination_params = {
                'TableName': table_name,
                'ReturnConsumedCapacity': 'TOTAL',
                'Limit': page_size,
            }
            if last_evaluated_key:
                pagination_params['ExclusiveStartKey'] = last_evaluated_key

            # Write items in the current page
            response = await asyncio.to_thread(dynamodb_client.batch_write_item,
                                               RequestItems={table_name: items})

            # Check if there are more pages to write
            if 'UnprocessedItems' in response and response['UnprocessedItems']:
                items = response['UnprocessedItems'][table_name]
                last_evaluated_key = response.get('LastEvaluatedKey')
            else:
                break

        return True
    except Exception as e:
        raise Exception(str(e))


def validate_delete_data_payload(data_list: list, hash_key: str):
    for data in data_list:
        if hash_key not in data.keys():
            raise Exception(f"Invalid payload, {hash_key} is missing")


# ========================= #
# delete an agent
# DELETE /db/rout_key/{hash_key_value}
# ========================= #


def handle_delete_item_from_dynamodb_with_hash_key(
        hash_key_value: str = None,
        hash_key_name: str = None,
        table_name: str = None,
        dynamodb_client: boto3.client = None):
    try:
        # check if agent_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=hash_key_value,
                key=hash_key_name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=hash_key_name,
                id=hash_key_value,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(err=None, res="delete data from dynamodb success")
    except Exception as e:
        raise Exception(str(e))


def handle_put_item_to_dynamodb_with_hash_key(hash_key_value: str,
                                              hash_key_name: str,
                                              request_body: dict,
                                              table_name: str = None,
                                              attributesTypeDict: dict = None,
                                              attributesEnum: Enum = None,
                                              dynamodb_client: boto3.client = None):

    try:
        # check if agent_id exists
        response = asyncio.run(
            get_item_from_dynamodb(
                id=hash_key_value,
                key=hash_key_name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError(f"{hash_key_name}: {hash_key_value} is not exist, please use post method to create a new"), res=None)
        else:
            # update item

            item = create_item(
                primary_key_name=hash_key_name,
                primary_key_value=hash_key_value,
                request_body=request_body,
                attributeType=attributesTypeDict,
                attributes=attributesEnum
            )
            # if not exist, put data in it
            response = asyncio.run(put_item_to_dynamodb(
                item=item,
                table_name=table_name,
                dynamodb_client=dynamodb_client,
            ))
            return respond(err=None, res="put an agent to dynamodb success")
    except Exception as e:
        raise Exception(str(e))


def handle_create_item_to_dynamodb(
        hash_key_name: str = None,
        hash_key_value: str = None,
        request_body: dict = None,
        table_name: str = None,
        attributeTypeDice=None,
        attributesEnum=None,
        dynamodb_client: boto3.client = None):

    try:
        # create a new agent
        # agent_id = str(guid())
        item = create_item(
            primary_key_name=hash_key_name,
            primary_key_value=hash_key_value,
            request_body=request_body,
            attributeType=attributeTypeDice,
            attributes=attributesEnum
        )
        response = asyncio.run(put_item_to_dynamodb(
            item=item,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
        ))
        created_item_hash_key = {
            hash_key_name: hash_key_value
        }
        return respond(err=None, res=json.dumps(created_item_hash_key))
    except Exception as e:
        raise Exception(str(e))


def handle_get_item_from_dynamodb_with_hash_key(
        hash_key_value: str = None,
        hash_key_name: str = None,
    attributesTypesDict: dict = None,
        dynamodb_client: boto3.client = None,
        table_name: str = None):
    try:
        response = asyncio.run(
            get_item_from_dynamodb(
                id=hash_key_value,
                key=hash_key_name,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            )
        )
        item = response.get('Item', None)
        if item is None:
            return respond(err=TESSError("no object is found"), res=None)
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            deserializer_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=attributesTypesDict)
            return respond(err=None, res=deserializer_data)
    except Exception as e:
        raise Exception(str(e))


def create_items_to_dynamodb(
        request_body: dict = None,
        dynamodb_client: boto3.client = None,
        table_name: str = None,
        hash_key_name: str = None,
        attributesTypeDict: dict = None,
):
    # check if data in request body is valid
    try:
        if 'data' not in request_body:
            raise KeyError("data is missing")
        json_data = request_body['data']
        # convert json data to dynamodb format
        dynamodb_items, created_hash_key_values = conver_josn_to_dynamodb_format(
            hash_key=hash_key_name,
            items=json_data,
            attributesType=attributesTypeDict)
        # put data to dynamodb
        response = asyncio.run(write_batch_items_to_dynamodb(
            chunks=dynamodb_items, table_name=table_name, dynamodb_client=dynamodb_client))

        return respond(err=None, res=json.dumps(created_hash_key_values))
    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)


def delete_items_from_dynamodb(
    request_body: str,
        dynamodb_client,
        table_name: str,
        hash_key_name: str,
):
    try:
        if 'data' not in request_body:
            raise KeyError("data is missing")
        delete_data_list = request_body['data']
        # validate data
        validate_delete_data_payload(
            data_list=delete_data_list, hash_key=hash_key_name)
        # delete data from dynamodb
        response = asyncio.run(delete_batch_items_from_dynamodb(
            chunks=delete_data_list, table_name=table_name, dynamodb_client=dynamodb_client))
        return respond(err=None, res="delete agents success")
    except Exception as e:
        return respond(err=TESSError(str(e)), res=None, status_code=500)
