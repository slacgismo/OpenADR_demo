import aiohttp
import logging


async def put_data(url: str, data: dict, timeout: int = 2, headers: dict = {'Content-Type': 'application/json'}):
    try:

        async with aiohttp.ClientSession() as session:
            logging.info(f"*********** Send to VTN API: {url} ***********")
            async with session.put(url, json=data, headers=headers, timeout=timeout) as response:
                return response

    except Exception as e:
        logging.error(f"Error VTN Submit to API: {e}")
        raise Exception(f"Error VTN Submit to API: {e}")
