
import uuid
import json
from decimal import Decimal
import asyncio
# Convert Decimal objects to float


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


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
        return respond(err=TESSError(str(e)), res=None, status_code=500)


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
    except Exception as e:
        raise Exception(e)


async def delete_item_from_dynamodb(key: str, id: str, table_name: str, dynamodb_client):
    try:
        response = await asyncio.to_thread(dynamodb_client.delete_item,
                                           TableName=table_name,
                                           Key={
                                               key: {'S': id}
                                           }
                                           )
        return respond(err=None, res=f"delete {key}: {id} from {table_name} success")

    except Exception as e:
        return respond(err=TESSError(str(e), None), res=None)
