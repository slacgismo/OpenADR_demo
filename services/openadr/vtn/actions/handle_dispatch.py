
from utils.convert import wait_till_next_market_end_time
import logging


async def handle_dispatch(
    order_id: str, tess_dispatch_api_url: str,
):
    """
    Submit the oder_id to dispatch and await for the response
    The response will be a quantity of the POWER
    """
    logging.info("handle  dispatch")
    # step 1 - submit the order_id to dispatch api: get
    # step 2 - wait for the response from dispatch, get quantity and price
    # step 3 - always send the price down to the VEN with the device_id
    # step 4 - if quantity is not 0, send the quantity the VEN. with the device_id

    # while True:

    #     payload = await get_data_from_api()
    #     message = json.loads(payload['message'])
    #     market_prices = message['market_prices']
    #     print(
    #         f"***** Fetched market_prices from API: {market_prices} ******* ")

    #     minutes_duration = 1
    #     for v in VENS.values():
    #         event_id = str(uuid.uuid4())
    #         server.add_event(ven_id=v['ven_id'],
    #                          signal_name=enums.SIGNAL_NAME.simple,
    #                          signal_type=enums.SIGNAL_TYPE.LEVEL,
    #                          intervals=[{'dtstart': datetime.now(timezone.utc),
    #                                     'duration': timedelta(minutes=int(minutes_duration)),
    #                                      'signal_payload': market_prices}],
    #                          callback=event_response_callback,
    #                          event_id=event_id,
    #                          )
    #     # Wait for x seconds before fetching the next market price
    #     await asyncio.sleep(MARKET_INTERVAL_IN_SECOND)
