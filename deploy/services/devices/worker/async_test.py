# # test


# import logging
# import asyncio
# import os
# import json
# import time
# from models_and_classes.ECS_ACTIONS_ENUM import ECS_ACTIONS_ENUM
# from handle_action import handle_action
# from models_and_classes.SQSService import SQSService
# from models_and_classes.HealthCheckHandler import HTTPServer
# from dotenv import load_dotenv
# import socketserver
# import time
# from handle_action import handle_action
# from app import process_task_from_fifo_sqs
# import aiohttp
# from aiohttp import web
# import aiohttp
# import asyncio
# load_dotenv()
# logging.basicConfig(format='%(asctime)s %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

# logging.info(f"Start the worker app")
# FIFO_SQS_URL = os.getenv('worker_fifo_sqs_url')
# if FIFO_SQS_URL is None:
#     raise Exception("FIFO_SQS_URL is not set")


# BACKEND_S3_BUCKET_NAME = os.getenv('backend_s3_bucket_devices_admin')
# if BACKEND_S3_BUCKET_NAME is None:
#     raise Exception("BACKEND_S3_BUCKET_NAME is not set")


# FIFO_DLQ_URL = os.getenv('worker_dlq_url')
# if FIFO_DLQ_URL is None:
#     raise Exception("FIFO_DLQ_URL is not set")

# AWS_REGION = os.getenv('aws_region')
# if AWS_REGION is None:
#     raise Exception("AWS_REGION is not set")

# DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME = os.getenv(
#     'dynamodb_agents_shared_remote_state_lock_table_name')
# if DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is None:
#     raise Exception(
#         "DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME is not set")


# def process_message(message):
#     # simulate processing time of 2 minutes
#     time.sleep(2)
#     print(f"Processed message: {message}")


# async def retrieve_messages():
#     # replace with your own code to retrieve messages from SQS
#     # messages = await get_messages_from_sqs()
#     print("start to receive message")
#     await process_task_from_fifo_sqs(
#         queue_url=FIFO_SQS_URL,
#         BACKEND_S3_BUCKET_NAME=BACKEND_S3_BUCKET_NAME,
#         DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME=DYNAMODB_AGENTS_SHARED_REMOTE_STATE_LOCK_TABLE_NAME,
#         AWS_REGION=AWS_REGION
#     )


# async def health_check():
#     server = HTTPServer()
#     await server.start()


# async def short_running_task():
#     await asyncio.sleep(2)
#     print(f"Short running {time.time()}")

#     # task1 = asyncio.create_task(health_check())
#     # task2 = asyncio.create_task(short_running_task())

#     # # wait for both tasks to complete
#     # await asyncio.gather(task1, task2)


# async def main():
#     server = HTTPServer()
#     # returns immediately, the task is created
#     task1 = asyncio.create_task(server.start('0.0.0.0', 8080))
#     await asyncio.sleep(3)
#     task2 = asyncio.create_task(retrieve_messages())
#     await task1
#     await task2


# if __name__ == '__main__':

#     # Run the client in the Python AsyncIO Event Loop

#     asyncio.run(main())  # main loop
