import logging
import aiohttp
import time


async def put_data_to_order_api_of_vtn(
    order_payload: dict = None,
    vtn_order_url: str = None,
):
    '''

    '''
    if order_payload is None or vtn_order_url is None:
        raise Exception(
            "data, vtn order cannot be None")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(vtn_order_url, json=order_payload) as response:
                if response.status != 200:
                    # TODO: handle 400, 401, 403, 404, 500
                    logging.error(
                        f"-------- VEN Submit order to Order API response status code: {response.status} --------")
                    return None, None, None
                else:
                    body = await response.json()
                    logging.info(
                        f"************ Submit to VTN Order API response body: {body} ************")

                    order_id = body.get('order_id')
                    quantity = body.get('quantity')
                    price = body.get('price')
                    return order_id, quantity, price

    except Exception as e:
        logging.error(f"Error submit order to Order API: {e}")
        raise Exception(f"Error checking Order API: {e}")


async def put_data_to_meter_api(
    data: dict = None,
    vtn_measurement_url: str = None,
):
    response = await pu_data(vtn_measurement_url, data)
    return response


async def submit_dispatch_to_vtn(
    vtn_dispatch_url: str = None,
    order_id: str = None,
    quantity: float = None,
):
    url = vtn_dispatch_url
    dispatch_data = {
        "order_id": order_id,
        "record_time": int(time.time()),
        "quantity": str(quantity)
    }
    logging.info("submit_dispatch_to_lambda ")
    response = await pu_data(url, dispatch_data)
    if response.status != 200:
        logging.warning(f"Error vtn submit order to VTN:{response} ")
        return None

    return await response.json()


async def pu_data(
    url: str = None,
    data: dict = None,
    timeout: int = 2,
    headers: dict = {'Content-Type': 'application/json'},
):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=data, timeout=timeout, headers=headers) as response:
                return response
    except Exception as e:
        raise Exception(f"VEN submit to VTN error: {e}")
