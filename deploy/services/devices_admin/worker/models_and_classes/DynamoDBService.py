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
    STATE = "state"


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
        response = self.table.get_item(
            Key={
                'agent_id': agent_id
            }
        )
        return response['Item']

    def update_item(self, agent_id, updates):
        try:
            self.table.update_item(
                Key={'agent_id': agent_id},
                UpdateExpression='SET ' +
                ', '.join([f"{k} = :{k}" for k in updates.keys()]),
                ExpressionAttributeValues={
                    f":{k}": v for k, v in updates.items()}
            )
        except ClientError as e:
            print(f"Error updating item: {e.response['Error']['Message']}")

    def qurey_item(self, agent_id):
        response = self.table.query(
            KeyConditionExpression=Key('agent_id').eq(agent_id)
        )
        return response['Items']

    def list_all_items_primary_id(self):
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


# import boto3
# from botocore.exceptions import ClientError

# class DynamoDBService:
#     def __init__(self, table_name):
#         self.table_name = table_name
#         self.dynamodb = boto3.resource('dynamodb')
#         self.table = self.dynamodb.Table(table_name)

#     def create_item(self, item):
    # try:
    #     self.table.put_item(Item=item)
    # except ClientError as e:
    #     print(f"Error creating item: {e.response['Error']['Message']}")

    # def delete_item(self, agent_id):
    #     try:
    #         self.table.delete_item(Key={'agent_id': agent_id})
    #     except ClientError as e:
    #         print(f"Error deleting item: {e.response['Error']['Message']}")

#     def delete_all_items(self):
#         try:
#             scan = self.table.scan()
#             with self.table.batch_writer() as batch:
#                 for item in scan['Items']:
#                     batch.delete_item(Key={'agent_id': item['agent_id']})
#         except ClientError as e:
#             print(f"Error deleting all items: {e.response['Error']['Message']}")

    # def list_number_of_items(self):
    #     try:
    #         count = self.table.item_count
    #         print(f"Number of items in table {self.table_name}: {count}")
    #     except ClientError as e:
    #         print(f"Error listing number of items: {e.response['Error']['Message']}")

    # def update_item(self, agent_id, updates):
    #     try:
    #         self.table.update_item(
    #             Key={'agent_id': agent_id},
    #             UpdateExpression='SET ' + ', '.join([f"{k} = :{k}" for k in updates.keys()]),
    #             ExpressionAttributeValues={f":{k}": v for k, v in updates.items()}
    #         )
    #     except ClientError as e:
    #         print(f"Error updating item: {e.response['Error']['Message']}")
