import datetime
import time
import logging
import asyncio


def convert_datetime_to_timsestamp(time_str: str) -> int:
    time_obj = datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    # convert datetime object to timestamp
    if not datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ'):
        raise Exception("time_str is not in the correct format")

    market_start_timestamp = int(time_obj.timestamp())
    return int(market_start_timestamp)


def next_market_start_timestamp(
    market_start_timestamp: str,
    market_interval: int,
) -> int:

    current_time = int(time.time())
    time_since_start = current_time - market_start_timestamp
    time_to_next_start = market_interval - \
        (time_since_start % market_interval)
    next_market_start_timestamp = current_time + time_to_next_start

    return next_market_start_timestamp


def current_market_start_timestamp(
    market_start_time: str,
    market_interval: int,
) -> int:
    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=market_start_time)
    current_time = int(time.time())
    time_since_start = current_time - market_start_timestamp
    time_to_next_start = (time_since_start % market_interval)
    if time_to_next_start == 0:
        return current_time
    else:
        # return previouse market start time
        return current_time + time_to_next_start - (market_interval)


# def time_to_next_markert_start_time(
#     current_time: int,
#     market_start_time: str,
#     market_interval: int,
# ) -> int:
#     market_start_timestamp = convert_datetime_to_timsestamp(
#         time_str=market_start_time)
#     current_time = int(time.time())
#     time_since_start = current_time - market_start_timestamp
#     time_to_next_start = (time_since_start % market_interval)

#     return time_to_next_start


async def wait_till_next_market_start_time(
        market_start_time: str,
        market_interval: int,
        advanced_seconds_of_market_startime: int = 0,
        funciton_name: str = None,
) -> int:
    if market_start_time is None:

        raise Exception("market_start_time is not set")
    if market_interval is None:
        raise Exception("market_interval is not set")
    # convert market_start_time to timestamp

    market_start_timestamp = convert_datetime_to_timsestamp(
        time_str=market_start_time)
    # get the current time
    current_time = int(time.time())
    time_since_start = current_time - \
        (market_start_timestamp - advanced_seconds_of_market_startime)
    time_to_next_start = market_interval - (time_since_start % market_interval)
    global_time_to_next_start = current_time + time_to_next_start
    # calculate the next marekt start timestamp

    while time_to_next_start > 0:
        await asyncio.sleep(1)
        time_to_next_start -= 1
        # if (time_to_next_start) % 1 == 0:
        #     logging.info(
        #         f"waiting..{time_to_next_start} seconds for {funciton_name} ")

    return time_to_next_start


# async def wait_till_next_market_end_time(market_start_time: str, market_interval: int) -> int:
#     """
#     Current start time is the previous end time
#     If we want to modify the end time, we can modify this funciton
#     """

#     if market_start_time is None:
#         raise Exception("market_start_time is not set")
#     if market_interval is None:
#         raise Exception("market_interval is not set")
#     # convert market_start_time to timestamp
#     market_start_timestamp = convert_datetime_to_timsestamp(
#         time_str=market_start_time)
#     # get the current time
#     current_time = int(time.time())

#     # calculate the next marekt start timestamp
#     # end time is the start time
#     time_since_start = current_time - market_start_timestamp
#     time_to_next_end = market_interval - (time_since_start % market_interval)

#     while time_to_next_end > 0:
#         await asyncio.sleep(1)
#         time_to_next_end -= 1
#         if time_to_next_end % 5 == 0:
#             logging.info(
#                 f"waiting for end of market ..{time_to_next_end} seconds")
#     logging.info("======================================")
#     logging.info("Market end time reached")
#     logging.info("======================================")
#     # current start time is the previous end time,
#     return time_to_next_end
