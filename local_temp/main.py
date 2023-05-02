from enum import Enum
import boto3
import asyncio
import time
from botocore.exceptions import ClientError
import json
import uuid
from decimal import Decimal
dynamodb_client = boto3.client('dynamodb')
agnets_table_name = 'openadr-NHEC-STAGING-agents'
agents_table_resource_id_valid_at_gsi = "resource_id_valid_at_index"


class AgentsAttributes(Enum):
    agent_id = 'agent_id'
    resource_id = 'resource_id'
    agent_status = 'agent_status'
    valid_at = 'valid_at'


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


class TESSError:
    def __init__(self, msg, exception=None):
        self.msg = msg
        self.exception = exception

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


AgentsAttributesTypes = {
    AgentsAttributes.agent_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.resource_id.name: {
        'dynamodb_type': 'S',
        'return_type': 'string'
    },
    AgentsAttributes.agent_status.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
    AgentsAttributes.valid_at.name: {
        'dynamodb_type': 'N',
        'return_type': 'integer'
    },
}


def create_agent_item(agent_id: str, resource_id: str, status: str, valid_at: str):
    item = {}
    for attribute_name, attribute_info in AgentsAttributesTypes.items():
        if attribute_name == AgentsAttributes.agent_id.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: agent_id
            }
        elif attribute_name == AgentsAttributes.resource_id.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: resource_id
            }
        elif attribute_name == AgentsAttributes.status.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: status
            }
        elif attribute_name == AgentsAttributes.valid_at.name:
            item[attribute_name] = {
                attribute_info['dynamodb_type']: str(valid_at)
            }
    return item


async def put_item_to_dynamodb(item: dict,
                               table_name: str,
                               dynamodb_client):
    try:

        response = await asyncio.to_thread(dynamodb_client.put_item,
                                           TableName=table_name,
                                           Item=item
                                           )
        return response

    except ClientError as e:
        raise ClientError(str(e))


async def get_item_from_dynamodb(id: str, key: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(
            dynamodb_client.get_item,
            TableName=table_name,
            Key={
                key: {'S': id}
            }
        )
        return response
    except ClientError as e:
        raise ClientError(str(e))


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


def put_list_of_agents_to_dynamodb(request_body: dict = None, dynamodb_client: boto3.client = None, table_name: str = None, limit_items: int = None):
    agents = request_body.get('agents', None)
    items = []
    for agent in agents:
        items.append(agent)
    chunks = [items[i:i+limit_items]
              for i in range(0, len(items), limit_items)]
    index = 0
    for chunk in chunks:
        # print("chunk : ", chunk)
        # conve
        print(f"Write file from  {index} to {index +limit_items }")
        response = asyncio.run(write_batch_items_to_dynambodb(
            chunks=chunk, table_name=table_name, dynamodb_client=dynamodb_client, limit_items=limit_items))
        index += limit_items
    return "success"


async def write_batch_items_to_dynamodb(chunks: list = None,
                                        table_name: str = None,
                                        dynamodb_client: boto3.client = None,
                                        page_size: int = 25):
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

        return response
    except Exception as e:
        raise Exception(str(e))


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
        end_at: str = None):
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

            for item in response.get('Items', []):
                item_dict = {}
                for key, value in item.items():
                    item_dict[key] = value.get('S', value.get('N'))
                items.append(item_dict)

            if 'LastEvaluatedKey' in response and response['LastEvaluatedKey']:
                last_evaluated_key = response['LastEvaluatedKey']
            else:
                break

        return items
    except Exception as e:
        raise Exception(str(e))


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


def guid():
    """Return a globally unique id"""
    return uuid.uuid4().hex[2:]


def create_agents(
    number_of_agents: int = None,
) -> dict:
    items = []
    for i in range(number_of_agents):
        agent_id = str(guid())
        resource_id = str(guid())
        status = "1"
        valid_at = str(int(time.time()))
        item = create_agent_item(agent_id=agent_id, resource_id=resource_id,
                                 status=status, valid_at=valid_at)
        item = {

            'agent_id': {'S': agent_id},
            'resource_id': {'S': resource_id},
            'status': {'N': status},
            'valid_at': {'N': valid_at},

        }
        items.append(item)
        time.sleep(1)
    return items


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


async def scan_dynamodb_table_with_pagination(key_name: str = None,
                                              key_value: str = None,
                                              key_type: str = 'S',
                                              page_size: int = 100,
                                              start_key: str = None,
                                              table_name: str = None,
                                              dynamodb_client: boto3.client = None):
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
        print("response", response)
        # Append the matching items to the result list
        items.extend(response['Items'])

        # Check if there are more items to retrieve
        if 'LastEvaluatedKey' in response:
            # If there are more items, update the start key and continue scanning
            start_key = response['LastEvaluatedKey']
            scan_params['ExclusiveStartKey'] = start_key
        else:
            # If there are no more items, stop scanning and return the result list
            break

    return items


def main():

    # agent_id = "123"
    # resource_id = "1122"
    # status = "1"
    # valid_at = int(time.time())
    # item = {
    #     AgentsAttributes.agent_id.value: {'S': agent_id},
    #     AgentsAttributes.resource_id.value: {'S': resource_id},
    #     AgentsAttributes.status.value: {'N': str(status)},
    #     AgentsAttributes.valid_at.name: {'N': str(valid_at)}
    # }
    # item = {
    #     AgentsAttributes.resource_id.name: {AgentsAttributes.resource_id.value['dynamobd_type']: resource_id},
    #     # AgentsAttributes.agent_id.name: {AgentsAttributes.agent_id.value['dynamobd_type']: agent_id},

    #     # AgentsAttributes.status.name: {AgentsAttributes.status.value['dynamobd_type']: status},
    #     # AgentsAttributes.valid_at.name: {
    #     #     AgentsAttributes.valid_at.value['dynamobd_type']: str(valid_at)}
    # }
    # put item
    try:
        # simulate payload
        test_agent_items = [
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '1'},
            {"resource_id": "1", 'agent_status': '0'},
        ]

        body = {'data': test_agent_items}
        payload = body['data']
        # # convet payload to dynamodb format
        dynamodb_items, created_items = conver_josn_to_dynamodb_format(
            hash_key='agent_id',
            items=payload,
            attributesType=AgentsAttributesTypes)
        # print(f"dynamodb_items {dynamodb_items}")

        # response = asyncio.run(write_batch_items_to_dynamodb(
        #     chunks=dynamodb_items, table_name=agnets_table_name, dynamodb_client=dynamodb_client, page_size=2))

        # print(json.dumps(created_hash_keys))
        # itmems = asyncio.run(scan_dynamodb_table_with_pagination(
        #     key_name='resource_id', key_value='1', table_name=agnets_table_name, dynamodb_client=dynamodb_client))
        # print(f"itmems :{itmems}")
        table_name = "openadr-NHEC-STAGING-resources"
        gsi_name = "resource_status_valid_at_index"
        items = asyncio.run(
            query_items_from_dynamodb_with_gsi(
                table_name=table_name,
                dynamodb_client=dynamodb_client,
                gsi_name=gsi_name,
                key_value='1',
                key_name='resource_status',
                key_type='N'
                # range_key='valid_at',
                # start_from=str(int(time.time()-20)),
            )
        )
        print("items", items)
        # check if items in response

        # delete_items = [
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"},
        #     {'agent_id': "7283ce527041a3a6e4f8cf1ea28220"}
        # ]
        # time.sleep(1)
        # response = asyncio.run(delete_batch_items_from_dynamodb(
        #     chunks=delete_items, table_name=agnets_table_name, dynamodb_client=dynamodb_client, page_size=2))
        # print(response)

        # items = create_agents(number_of_agents=10)
        # print(items)
        # put_list_of_agents_to_dynamodb(request_body={'agents': items},
        #                                dynamodb_client=dynamodb_client,
        #                                table_name=agnets_table_name,
        #                                limit_items=2)
        # item = create_item(agent_id=agent_id, resource_id=resource_id,
        #                    status=status, valid_at=valid_at)
        # print(item)
        # response = asyncio.run(put_item_to_dynamodb(
        #     item=item, table_name=agnets_table_name, dynamodb_client=dynamodb_client))
        # print(response)
        # agent_id = "123"
        # response = asyncio.run(get_item_from_dynamodb(
        #     id=agent_id, key='agent_id', table_name=agnets_table_name, dynamodb_client=dynamodb_client))
        # item = response.get('Item', None)
        # agent_data = deserializer_dynamodb_data_to_json_format(
        #     item=item, attributesTypes=AgentsAttributesTypes)
        # print(agent_data)
        # response = asyncio.run(delete_item_from_dynamodb(
        #     id=agent_id, key='agent_id', table_name=agnets_table_name, dynamodb_client=dynamodb_client))

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
