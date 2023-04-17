# import logging
# import asyncio
# import aiohttp
# import json


# async def check_device_id_from_tess_device_api(
#     ven_id: str,
#     device_id: str,
#     agent_id: str,
#     resource_id: str,
#     DEVICES_API_URL: str,
# ):
#     logging.info(
#         "Check device id, agent_id, and resource id from tess device api")
#     async with aiohttp.ClientSession() as session:
#         async with session.get(DEVICES_API_URL+f"/{device_id}") as response:
#             content_type = response.headers.get('Content-Type', '')
#             if 'application/json' not in content_type:
#                 raise Exception(f"Unexpected content type: {content_type}")
#             try:
#                 body = await response.json()
#                 logging.info(f"Check device id from tess device api: {body}")
#             except Exception as e:
#                 logging.error(f"Check device id failed {e}")
#                 return None
#             return response
