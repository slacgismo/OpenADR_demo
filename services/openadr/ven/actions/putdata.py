import logging
import aiohttp


async def put_data(url: str, data: dict, headers: dict = {'Content-Type': 'application/json'}, timeout: int = 2):
    try:
        async with aiohttp.ClientSession() as session:
            logging.info(f"*********** Send to VTN API: {url} ***********")
            async with session.put(url, json=data, headers=headers, timeout=timeout) as response:
                return response
    except Exception as e:
        raise Exception(f"Error VTN API: {e}")
