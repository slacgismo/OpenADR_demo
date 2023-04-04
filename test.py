
import aiohttp
import asyncio
import json
import logging


async def sumbit_oder_to_oder_api(
    device_id: str = None,
    resource_id: str = None,
    record_time: str = None,
    quantity: str = None,
    flexible: str = None,
    state: str = None,
    ORDERS_PAI_URL: str = None,
):
    """
    PUT /order/{device_id}
    """

    data = {
        'resource_id': resource_id,
        'quantity': quantity,
        'record_time': record_time,
        'flexible': flexible,
        'state': state
    }
    order_url = ORDERS_PAI_URL+f"/{device_id}"
    print(
        f" **************put {order_url }=====================================")
    try:

        print()
        async with aiohttp.ClientSession() as session:
            async with session.put(order_url, json=data) as response:

                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    raise Exception(f"Unexpected content type: {content_type}")

                response_body = await response.text()
                response_json = json.loads(response_body)
                print(response_json)
                return response_json

    except Exception as e:
        raise Exception(f"Error submit order to TESS: {e}")


async def submit_meter_to_meter_url(
    device_id: str = None,
    meter_id: str = None,
    resource_id: str = None,
    real_energy: str = None,
    reactive_energy: str = None,
    real_power: str = None,
    reactive_power: str = None,
    METERS_API_URL: str = None,
):
    """
    Submit the oder_id to dispatch and await for the response
    The response will be a quantity of the POWER
    PUT /meter/{device_id}/{meter_id}
    """

    meter_url = METERS_API_URL + "/" + device_id + "/" + meter_id
    print(f"send device data to TESS meter  api: {device_id}/{meter_id}")
    data = {
        "resource_id": resource_id,
        "real_energy": real_energy,
        "reactive_energy": reactive_energy,
        "real_power": real_power,
        "reactive_power": reactive_power,
    }
    print(
        f"send device data to TESS meter  api: {device_id}/{meter_id}")
    async with aiohttp.ClientSession() as session:
        async with session.put(meter_url, json=data) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                raise Exception(f"Unexpected content type: {content_type}")
            try:
                body = await response.json()
                print(f"meter response: {body}")
            except Exception as e:
                raise Exception(f"Error parse response: {e}")
            return response


loop = asyncio.new_event_loop()
# loop.create_task(sumbit_oder_to_oder_api(
#     device_id="320d141048c23741139cc30262369a86",
#     resource_id="123",
#     record_time="123",
#     quantity="123",
#     flexible="123",
#     state="123",
#     ORDERS_PAI_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/order"
# ))
loop.create_task(submit_meter_to_meter_url(
    device_id="320d141048c23741139cc30262369a86",
    meter_id="320d141048c23741139cc30262369a86",
    resource_id="320d141048c23741139cc30262369a86",
    real_energy=1000,
    reactive_energy=None,
    real_power=None,
    reactive_power=None,
    METERS_API_URL="https://w6lgi4v3le.execute-api.us-east-2.amazonaws.com/dev/meter"
))
loop.run_forever()
