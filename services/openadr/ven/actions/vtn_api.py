import logging
import aiohttp
import time


async def put_data_to_order_api_of_vtn(
    resource_id: str = None,
    flexible: str = None,
    state: str = None,

    vtn_order_url: str = None,
):
    '''
    send payload 
    PUT /order/{device_id}
    {
        resource_id
        flexible
        state

    }

    return {
        order_id
        quantity
        price
    }

    '''

    order_payload = {
        'resource_id': resource_id,
        'flexible': flexible,
        'state': state
    }

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
                    # logging.info(
                    #     f"************ Submit to VTN Order API response body: {body} ************")

                    order_id = body.get('order_id')
                    quantity = body.get('quantity')
                    price = body.get('price')
                    return order_id, quantity, price

    except Exception as e:
        logging.error(f"Error submit order to Order API: {e}")
        raise Exception(f"Error checking Order API: {e}")


async def submit_dispatch_to_vtn(
    vtn_dispatch_url: str = None,
    order_id: str = None,
    quantity: float = None,
    headers: dict = {'Content-Type': 'application/json'},
    timeout: int = 2
):
    '''
    PUT /dispatch/{order_id}
    send {
        order_id
        record_time
        quantity
    }
    return {
        quantity
        price
    }
    '''

    dispatch_data = {
        "order_id": order_id,
        "record_time": int(time.time()),
        "quantity": str(quantity)
    }

    logging.info("submit_dispatch_to_lambda ")
    async with aiohttp.ClientSession() as session:
        async with session.put(url=vtn_dispatch_url, json=dispatch_data, timeout=timeout, headers=headers) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                text = await response.text()
                logging.error(
                    f"Unexpected content type: {content_type} {text}")
                raise Exception(f"Unexpected content type: {content_type}")
            if response.status != 200:
                logging.info(f"Error submit order to TESS:{response} ")
                raise Exception(
                    f"Error submit order to TESS: {response.status}")
            return await response.json()


async def put_data_to_meter_api(
    readings: str = None,
    device_id: str = None,
    meter_id: str = None,
    resource_id: str = None,
    device_brand: str = None,
    status: str = None,
    timestamp: str = None,
    vtn_measurement_url: str = None,
    timeout: int = 2,
    headers: dict = {'Content-Type': 'application/json'},
):
    '''
    PUT /meter/{device_id}/{meter_id}
    send {
        readings
        device_id
        meter_id
        resource_id
        device_brand
        status
        timestamp
    }
    return {
        None
    }
    '''
    data = {
        "readings": readings,
        "device_id": device_id,
        "meter_id": meter_id,
        "resource_id": resource_id,
        "device_brand": device_brand,
        "status": status,
        "timestamp": timestamp
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.put(url=vtn_measurement_url, json=data, timeout=timeout, headers=headers) as response:
                if await response.status != 200:
                    return False
                return True
    except Exception as e:
        raise Exception(f"Error checking Meter API: {e}")
