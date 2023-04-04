

import logging
import aiohttp


async def handle_dispatch(
    order_id: str, DISPATCHES_API_URL: str,
):
    """
    Submit the oder_id to dispatch and await for the response
    The response will be a quantity of the POWER
    GET /dispatch/{order_id}
    """
    url = DISPATCHES_API_URL + "/" + order_id
    logging.info(
        f"send dispatch request to TESS dispatch api: {order_id}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                raise Exception(f"Unexpected content type: {content_type}")
            try:
                body = await response.json()
            except Exception as e:
                logging.error(f"Dispatch failed {e}")
                return None
            return response
