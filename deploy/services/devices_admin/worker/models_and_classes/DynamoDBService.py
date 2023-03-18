import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from enum import Enum


class DynamoDB_Key(Enum):
    AGENT_ID = "agent_id"
    RESOURCE_ID = "resource_id"
    VTN_ID = "vtn_id"
    VENS = "vens"
    VALID_AT = "valid_at"
    BACKEND_S3_STATE_KEY = "backend_s3_state_key"
    BACKEND_DYNAMODB_LOCK_NAME = "backend_dynamodb_lock_name"
    TASK_DEFINITION_FILE_NAME = "task_definition_file_name"
    CURRENT_STATUS = "current_status"


class DynamoDBService:
    def __init__(self, table_name):

        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)
     # check table exist

    def check_if_table_exist(self):
        try:
            self.dynamodb.meta.client.describe_table(TableName=self.table_name)
            print("Table exist")
            return True
        except ClientError as e:
            print("Table does not exist")
            return False

    def create_item(self, item):
        try:
            self.table.put_item(Item=item)
            print("Item created on DynamoDB")
        except ClientError as e:
            print(f"Error creating item: {e.response['Error']['Message']}")

    def check_if_agent_id_exist(self, agent_id: str) -> bool:
        try:
            response = self.table.get_item(
                Key={
                    'agent_id': agent_id
                }
            )
            if 'Item' in response:
                return True
            else:
                return False
        except ClientError as e:
            print(
                f"Error checking if agent_id exist: {e.response['Error']['Message']}")

    def get_item(self, agent_id):
        try:
            response = self.table.get_item(
                Key={
                    'agent_id': agent_id
                }
            )
            if 'Item' in response:
                return response['Item']
            else:
                return None

        except ClientError as e:
            raise f"Error getting item: {e.response['Error']['Message']}"

    def upate_items(self, agent_id: str, update_keys_values: dict):
        update_expression = 'SET '
        expression_attribute_values = {}
        for key, value in update_keys_values.items():
            update_expression += '{} = :{},'.format(key, key)
            expression_attribute_values[':{}'.format(key)] = value
        update_expression = update_expression.rstrip(',')
        # remove key from dynamodb
        try:
            # Update the item with the given primary key and update expression
            self.table.update_item(
                Key={
                    'agent_id': agent_id
                },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        except ClientError as e:
            raise f"Error updating item: {e.response['Error']['Message']}"

    def remove_keys_from_item(self, agent_id: str, keys_to_remove: list):
        update_expression = 'REMOVE '
        for key in keys_to_remove:
            update_expression += '{},'.format(key)
        update_expression = update_expression.rstrip(',')
        # remove key from dynamodb
        try:
            # Update the item with the given primary key and update expression
            self.table.update_item(
                Key={
                    'agent_id': agent_id
                },
                UpdateExpression=update_expression
            )
        except ClientError as e:
            raise f"Error updating item: {e.response['Error']['Message']}"

    def qurey_item(self, agent_id):
        response = self.table.query(
            KeyConditionExpression=Key('agent_id').eq(agent_id)
        )
        return response['Items']

    def list_all_items_primary_id(self, primary_id: str):
        response = self.client.scan(
            TableName=self.table_name,
            ProjectionExpression='agent_id'
        )
        return [item['id'] for item in response['Items']]

    def delete_item(self, agent_id):
        try:
            self.table.delete_item(Key={'agent_id': agent_id})
            print(f"Item {agent_id} deleted from DynamoDB")
        except ClientError as e:
            print(f"Error deleting item: {e.response['Error']['Message']}")

    def list_number_of_items(self):
        try:
            count = self.table.item_count
            print(f"Number of items in table {self.table_name}: {count}")
        except ClientError as e:
            print(
                f"Error listing number of items: {e.response['Error']['Message']}")
