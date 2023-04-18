

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
            " =================== handle_dispatch: =========================================")
        async with aiohttp.ClientSession() as session:
            async with session.get(DISPATCHES_API_URL+f"/{order_id}") as response:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    message = response.text()
                    raise Exception(
                        f"Unexpected content type: {content_type} message {message}")
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
