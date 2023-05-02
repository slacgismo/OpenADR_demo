
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


class GetItemsActions(Enum):
    query = "query"
    scan = "scan"


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


class QueryStringParametersOfQuery(Enum):
    gsi_name = 'gsi_name'
    key_value = 'key_value'
    key_name = 'key_name'
    key_type = 'key_type'
    range_key = 'range_key'
    range_key_value = 'range_key_value'
    range_key_type = 'range_key_type'
    start_from = 'start_from'
    end_at = 'end_at'


class QueryStringParametersOfScan(Enum):
    key_name = 'key_name'
    key_value = 'key_value'
    key_type = 'key_type'


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


def respond(err=None, res_message: str = None, res_data: dict = None,  status_code=200):
    response_body = {}
    if err:
        response_body['error'] = err.msg
        if status_code == 200:
            status_code = 400
    else:
        if res_message is not None:
            response_body['message'] = res_message
        if res_data is not None:
            response_body['data'] = res_data

    return {
        'statusCode': str(status_code),
        'body': json.dumps(response_body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


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


def deserializer_dynamodb_data_to_json_format(
        item: dict,
        attributesTypes: dict):
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
            raise KeyError(
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
    return_item = {}
    valid_at = str(int(time.time()))
    for attribute_name, attribute_info in attributeType.items():
        if attribute_name == attributes.valid_at.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: valid_at
            }
            return_item[attribute_name] = valid_at
        elif attribute_name == primary_key_name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: primary_key_value
            }
            return_item[attribute_name] = primary_key_value
        else:
            value = request_body.get(attribute_name, None)
            if value is None:
                raise KeyError(f"{attribute_name} not exist in request body.")
            item[attribute_name] = {
                attribute_info['dynamodb_type']: value
            }
            return_item[attribute_name] = value
    return item, return_item


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
    created_items = []
    for item in items:
        dynamodb_item = {}
        single_item = {}
        for key, value in attributesType.items():
            print(key, value['dynamodb_type'])
            dynamodb_type = value['dynamodb_type']
            # valid at is the current timestamp
            if key == timestam_index_name:
                item_value = str(int(time.time()))
                single_item[timestam_index_name] = item_value
            # create a unique id for hash key
            elif key == hash_key:
                item_value = str(guid())
                # hash_key_item = {hash_key: item_value}
                single_item[hash_key] = item_value
                # created_items.append(hash_key_item)
            else:
                item_value = item[key]
                single_item[key] = item_value
            dynamodb_item[key] = {dynamodb_type: item_value}

        created_items.append(single_item)
        dynamodb_items.append(dynamodb_item)
    # print(dynamodb_items)
    return dynamodb_items, created_items


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


# ======================================================#
# Delete a item from dynamodb with hash key  #
# ======================================================#


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
            return respond(err=TESSError("no object is found"))
        else:
            # if exists, delete it
            response = asyncio.run(delete_item_from_dynamodb(
                key=hash_key_name,
                id=hash_key_value,
                table_name=table_name,
                dynamodb_client=dynamodb_client
            ))
            return respond(res_message="success")
    except Exception as e:
        raise Exception(str(e))

# ======================================================#
# Update a item from dynamodb with hash key  #
# ======================================================#


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
            return respond(err=TESSError(f"{hash_key_name}: {hash_key_value} is not exist, please use post method to create a new"))
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

            return respond(res_message="success")
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
        item, return_item = create_item(
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
        # created_item_hash_key = {
        #     hash_key_name: hash_key_value
        # }
        return respond(res_data=json.dumps(return_item))
    except Exception as e:
        raise Exception(str(e))
# ======================================================#
# Get a item from dynamodb with hash key  #
# ======================================================#


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
            return respond(err=TESSError("no object is found"))
        else:
            # Lazy-eval the dynamodb attribute (boto3 is dynamic!)
            deserializer_data = deserializer_dynamodb_data_to_json_format(
                item=item, attributesTypes=attributesTypesDict)
            return respond(res_data=deserializer_data)
    except Exception as e:
        raise Exception(str(e))

# ======================================================#
# Create items from dynamodb  #
# ======================================================#


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
        dynamodb_items, created_items = conver_josn_to_dynamodb_format(
            hash_key=hash_key_name,
            items=json_data,
            attributesType=attributesTypeDict)
        # put data to dynamodb
        response = asyncio.run(write_batch_items_to_dynamodb(
            chunks=dynamodb_items, table_name=table_name, dynamodb_client=dynamodb_client))

        return respond(res_data=json.dumps(created_items))
    except Exception as e:
        return respond(err=TESSError(str(e)))


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

        return respond(res_message="success")
    except Exception as e:
        return respond(err=TESSError(str(e)))

# ======================================================#
# Query items from dynamodb  with global secondary index#
# ======================================================#


async def query_items_from_dynamodb_with_gsi(
        table_name: str = None,
        gsi_name: str = None,
        key_value: str = None,
        key_name: str = None,
        key_type: str = 'S',
        dynamodb_client: boto3.client = None,
        page_size: int = 25,
        range_key: str = None,
        range_key_type: str = 'N',
        start_from: str = None,
        end_at: str = None,
        attributes_types_dict: dict = None,
):
    """
    Query items from dynamodb with global secondary index
    if range_key is not None, query items with range key
        if start_from is not None, and end_at is None, query items from start_from to end
        if start_from is None, and end_at is not None, query items from start to end_at
        if start_from is not None, and end_at is not None, query items from start_from to end_at
    params: table_name: name of table
    params: gsi_name: name of global secondary index
    params: key_value: value of key (hash key value of global secondary index)
    params: key_name: name of key (hash key name of global secondary index)
    params: key_type: type of key (hash key type of global secondary index)
    params: dynamodb_client: dynamodb client
    params: page_size: number of items per page
    params: range_key: name of range key
    params: range_key_type: type of range key
    params: start_from: start from range key value
    params: end_at: end at range key value
    return: list of items
    """
    try:
        items = []
        last_evaluated_key = None
        # condition_expression = f"{hash_key} = :{hash_key}"
        if gsi_name is None:
            key_condition_expression = f"{key_name} = :{key_name}"
            expression_attribute_values = {
                f':{key_name}': {key_type: key_value}}
        elif start_from is None and end_at is None:
            key_condition_expression = f"{key_name} = :{key_name}"
            expression_attribute_values = {
                f':{key_name}': {key_type: key_value}}
        elif start_from is None and end_at is not None:
            key_condition_expression = f"{key_name} = :{key_name} AND {range_key} <= :end_at"
            expression_attribute_values = {
                f':{key_name}': {key_type: key_name},
                ':end_at': {range_key_type: str(end_at)}
            }
        elif start_from is not None and end_at is None:
            key_condition_expression = f"{key_name} = :{key_name} AND {range_key} >= :start_from"
            expression_attribute_values = {
                f':{key_name}': {key_type: key_value},
                ':start_from': {range_key_type: str(start_from)}
            }
        else:
            key_condition_expression = f"{key_name} = :{key_name} AND {range_key} BETWEEN :start_from AND :end_at"
            expression_attribute_values = {
                f':{key_name}': {key_type: key_value},
                ':start_from': {range_key_type: str(start_from)},
                ':end_at': {range_key_type: str(end_at)}
            }
        # perform pagination
        while True:
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

            response = await asyncio.to_thread(dynamodb_client.query, **pagination_params)

            # convert dynamodb data to json format
            for item in response.get('Items', []):
                item_dict = deserializer_dynamodb_data_to_json_format(
                    item=item, attributesTypes=attributes_types_dict)
                items.append(item_dict)
                # for key, value in item.items():
                #     item_dict[key] = value.get('S', value.get('N'))
                # items.append(item_dict)

            if 'LastEvaluatedKey' in response and response['LastEvaluatedKey']:
                last_evaluated_key = response['LastEvaluatedKey']
            else:
                break

        return items
    except Exception as e:
        raise Exception(str(e))

# ======================================================#
# Scan items from dynamodb #
# ======================================================#


async def scan_dynamodb_table_with_pagination(key_name: str = None,
                                              key_value: str = None,
                                              key_type: str = 'S',
                                              page_size: int = 100,
                                              start_key: str = None,
                                              table_name: str = None,
                                              dynamodb_client: boto3.client = None,
                                              attributes_types_dict: dict = None):
    """
    Scan all items from dynamodb table with pagination with key that is nor primary key or global secondary index
    params: key_name: name of key
    params: key_value: value of key
    params: key_type: type of key
    """
    # Define the parameters for the scan
    if key_name is None or key_value is None:
        raise Exception('key_name or key_value is required')
    table_name = table_name
    filter_expression = f'{key_name} = :id'
    expression_attribute_values = {
        ':id': {key_type: str(key_value)}
    }

    # Create an empty list to store the matching items
    items = []

    # Set the initial parameters for the scan
    scan_params = {
        'TableName': table_name,
        'FilterExpression': filter_expression,
        'ExpressionAttributeValues': expression_attribute_values,
        'Limit': page_size,
        'Select': 'ALL_ATTRIBUTES'
    }

    # If there is a start key from a previous scan, use it to resume the scan
    if start_key:
        scan_params['ExclusiveStartKey'] = start_key

    # Scan the table until there are no more items to retrieve
    while True:
        # Execute the scan with the current parameters
        response = await asyncio.to_thread(dynamodb_client.scan, **scan_params)

        # convert dynamodb data to json format
        for item in response.get('Items', []):
            item_dict = deserializer_dynamodb_data_to_json_format(
                item=item,
                attributesTypes=attributes_types_dict
            )
            items.append(item_dict)
        # Check if there are more items to retrieve
        if 'LastEvaluatedKey' in response:
            # If there are more items, update the start key and continue scanning
            start_key = response['LastEvaluatedKey']
            scan_params['ExclusiveStartKey'] = start_key
        else:
            # If there are no more items, stop scanning and return the result list
            break

    return items


def handle_query_items_from_dynamodb(
    query_string_parameters: dict,
    table_name: str,
    environment_variables_list: set,
    dynamodb_client: boto3.client,
    attributes_types_dict: dict,

):

    gsi_name = query_string_parameters.get(
        QueryStringParametersOfQuery.gsi_name.value, None)
    key_value = query_string_parameters.get(
        QueryStringParametersOfQuery.key_value.value, None)
    key_name = query_string_parameters.get(
        QueryStringParametersOfQuery.key_name.value, None)
    if gsi_name is None or key_value is None or key_name is None:
        raise Exception(
            f"gsi_name, key_value, key_name are required for query action")

    key_type = query_string_parameters.get(
        QueryStringParametersOfQuery.key_type.value, None)
    range_key = query_string_parameters.get(
        QueryStringParametersOfQuery.range_key.value, None)
    range_key_type = query_string_parameters.get(
        QueryStringParametersOfQuery.range_key_type.value, None)
    start_from = query_string_parameters.get(
        QueryStringParametersOfQuery.start_from.value, None)
    end_at = query_string_parameters.get(
        QueryStringParametersOfQuery.end_at.value, None)
    # check if the key_type is valid
    if key_type is not None and key_type not in attributes_types_dict[key_name]['dynamodb_type']:
        raise Exception(f"key_type {key_type} is not valid")
    if key_type is None:
        key_type = 'S'
    # check if the key_name is valid
    if key_name is not None and key_name not in attributes_types_dict:
        raise Exception(
            f"key_name {key_name} is not valid")

    # check if the range_key is valid
    if range_key is not None and range_key not in attributes_types_dict:
        raise Exception(f"range_key {range_key} is not valid")

    # check if the gsi_name is valid
    if range_key is not None and range_key_type not in attributes_types_dict[key_name]['dynamodb_type']:
        raise Exception(f"range_key_type {range_key_type} is not valid")
    if gsi_name is None or gsi_name not in environment_variables_list:
        raise Exception(f"gsi_name {gsi_name} is not valid")
    items = asyncio.run(
        query_items_from_dynamodb_with_gsi(
            table_name=table_name,
            dynamodb_client=dynamodb_client,
            gsi_name=gsi_name,
            key_value=key_value,
            key_name=key_name,
            key_type=key_type,
            range_key=range_key,
            range_key_type=range_key_type,
            start_from=start_from,
            end_at=end_at,
            attributes_types_dict=attributes_types_dict
        )
    )
    return respond(res_data=items)


def handle_scan_items_from_dynamodb(
    query_string_parameters: dict,
    table_name: str,
    dynamodb_client,
    attributes_types_dict: dict,
):
    key_name = query_string_parameters.get(
        QueryStringParametersOfScan.key_name.value, None)
    key_value = query_string_parameters.get(
        QueryStringParametersOfScan.key_value.value, None)
    key_type = query_string_parameters.get(
        QueryStringParametersOfScan.key_type.value, None)
    if key_name is None or key_value is None:
        raise Exception(
            f"key_name, key_value are required for scan action")
    # check if key_name is valid
    if key_name not in attributes_types_dict:
        raise Exception(
            f"key_name {key_name} is not in {attributes_types_dict}")
    # check if key_type is valid
    if key_type is not None and key_type not in attributes_types_dict[key_name]['dynamodb_type']:
        raise Exception(f"key_type {key_type} is not valid")
    # default key_type to string
    if key_type is None:
        key_type = 'S'
    # perform scan
    items = asyncio.run(
        scan_dynamodb_table_with_pagination(
            key_name=key_name,
            key_value=key_value,
            key_type=key_type,
            table_name=table_name,
            dynamodb_client=dynamodb_client,
            attributes_types_dict=attributes_types_dict,
        ))
    # items = {"key_name": key_name, "key_value": key_value}
    return respond(res_data=items)


def match_path(split_prefix: str = "/db/", path: str = None, route_key: str = None) -> bool:
    """
    match the path with route_key
    :param split_prefix: the prefix to split the path, default is "/db/"
    :param path: the path
    :param route_key: the route_key
    :return: True if match, False if not match
    """
    if "/db/" in path:
        path_suffix = path.split(split_prefix)[1]
        if path_suffix == route_key:
            return True
    return False
