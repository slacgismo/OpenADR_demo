import asyncio
import logging
from aiohttp import web


async def handle_health_check(request):
    """
    Handle a trigger event request.
    """
    try:

        return web.json_response(f"ok", status=200)
    except Exception as e:
        # Bad path where name is not set
        response_obj = {'status': 'failed', 'info': str(e)}
        # return failed with a status code of 500 i.e. 'Server Error'
        return web.json_response(response_obj, status=500)
