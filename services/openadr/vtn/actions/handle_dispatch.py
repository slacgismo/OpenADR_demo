

import logging
import aiohttp
from aiohttp import web


async def handle_dispatch(
    request,
    DISPATCHES_API_URL: str,
):
    try:

        ven_id = request.match_info['ven_id']
        body = await request.json()
        order_id = body['order_id']
        logging.info(
            "handle_dispatch: =========================================")
        async with aiohttp.ClientSession() as session:
            async with session.get(DISPATCHES_API_URL+f"/{order_id}") as response:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    logging.error(f"Unexpected content type: {content_type}")
                    raise Exception(f"Unexpected content type: {content_type}")
                try:
                    logging.info(
                        f"Check device id from tess device api: {await response.json()}")
                    return web.json_response(await response.json(), status=200)

                except Exception as e:
                    logging.error(f"Check device id failed {e}")
                    return web.json_response({'status': 'failed', 'info': str(e)}, status=500)
    except Exception as e:
        logging.error(f"Error handle dispatch: {e}")
        return web.json_response({'status': 'failed', 'info': str(e)}, status=500)


# async def handle_dispatch(
#         request,
#     DISPATCHES_API_URL: str,
# ):
#     """
#     Submit the oder_id to dispatch and await for the response
#     The response will be a quantity of the POWER
#     GET /dispatch/{order_id}


#     """
#     try:
#         ven_id = request.match_info['ven_id']
#         dispatch_data = await request.json()
#         logging.info("=========================================")
#         logging.info(f"handle_dispatch: {dispatch_data}")
#         if 'order_id' not in dispatch_data:
#             raise Exception(f"Error parse order data: {dispatch_data}")
#         order_id = dispatch_data['order_id']
#         order_id = None
#         for key, value in dispatch_data.items():
#             if key == 'order_id':
#                 order_id = value
#             logging.info(f"{key}: {value}")
#         if order_id is None:
#             raise Exception(f"Error parse order data: {dispatch_data}")

#         url = DISPATCHES_API_URL + "/" + order_id

#         logging.info(
#             f"send dispatch request to TESS dispatch api: {url}")
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url=url) as response:
#                 content_type = response.headers.get('Content-Type', '')
#                 if 'application/json' not in content_type:
#                     return web.json_response({'status': 'failed', 'info': f"{content_type} not correct"}, status=500)
#                 if response.status != 200:
#                     return web.json_response({'status': 'failed', 'info': str(response.json)}, status=500)
#                 return response
#     except Exception as e:
#         logging.error(f"Dispatch failed {e}")
#         return web.json_response({'status': 'failed', 'info': str(e)}, status=500)
#         # if response.status != 200:
#         #     raise Exception(
#         #         f"Error submit order to TESS: {response.status}")
#         # try:
#         #     body = await response.json()
#         #     return body
#         # except Exception as e:
#         #     logging.error(f"Dispatch failed {e}")
#         #     return None
