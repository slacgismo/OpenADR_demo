import logging
from .handle_dispatch import handle_dispatch
from models_classes.SharedDeviceInfo import SharedDeviceInfo
import json


async def handle_event(event, shared_device_info: SharedDeviceInfo):
    # This callback receives an Event dict.
    try:

        if 'targets' not in event:
            logging.error(f"******** {event} ********")
        if len(event['targets']):
            ven_id = event['targets'][0]['ven_id']
            signal_payload = event['event_signals'][0]['intervals'][0]['signal_payload']
            signal_name = event['event_signals'][0]['signal_name']
            signal_type = event['event_signals'][0]['signal_type']
            logging.info("================= EVENT PRICE ===================")
            logging.info(
                f"******** {ven_id} get event: {signal_name} {signal_type} {signal_payload} ********")

    except Exception as e:
        logging.error(f"Error pase event: {e}")
    return 'optIn'
