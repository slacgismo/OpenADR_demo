import datetime
import logging
import time
import asyncio


def convert_datetime_to_timsestamp(time_str: str) -> int:
    time_obj = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    # convert datetime object to timestamp
    if not datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ'):
        raise Exception("time_str is not in the correct format")

    market_start_timestamp = int(time_obj.timestamp())
    return int(market_start_timestamp)


async def wait_till_next_market_end_time(market_start_time: str, market_interval: int) -> int:
    """
    Current start time is the previous end time
    If we want to modify the end time, we can modify this funciton
    """
    if market_start_time is None:
        raise Exception("market_start_time is not set")
    if market_interval is None:
        raise Exception("market_interval is not set")
    # convert market_start_time to timestamp
    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=market_start_time)
    # get the current time
    current_time = int(time.time())

    # calculate the next marekt start timestamp
    # end time is the start time
    time_since_start = current_time - market_start_timestamp
    time_to_next_start = market_interval - (time_since_start % market_interval)

    logging.info("======================================")
    logging.info(
        f"current_time: {current_time}, market_start_timestamp: {market_start_timestamp}, time_to_wait: {time_to_next_start}")

    logging.info("======================================")
    while time_to_next_start > 0:
        await asyncio.sleep(1)
        time_to_next_start -= 1
        # logging.info(f"waiting for end of market ..{time_to_wait} seconds")
    logging.info("======================================")
    logging.info("Market end time reached")
    logging.info("======================================")
    # current start time is the previous end time,
    return time_to_next_start
