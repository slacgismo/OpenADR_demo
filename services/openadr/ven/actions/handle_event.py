import logging
from .handle_dispatch import handle_dispatch
from models_classes.SharedDeviceInfo import SharedDeviceInfo


async def handle_event(event, shared_device_info: SharedDeviceInfo):
    # This callback receives an Event dict.
    try:

        device_settings = shared_device_info.get_device_settings()
        device_type = shared_device_info.get_device_type()
        is_using_mock_device = shared_device_info.get_is_using_mock_device()
        emulated_device_api_url = shared_device_info.get_emulated_device_api_url()

        if 'targets' not in event:
            logging.error(f"******** {event} ********")
        if len(event['targets']):
            ven_id = event['targets'][0]['ven_id']
            signal_payload = event['event_signals'][0]['intervals'][0]['signal_payload']
            signal_name = event['event_signals'][0]['signal_name']
            signal_type = event['event_signals'][0]['signal_type']
            logging.info(
                f"******** {ven_id} get event: {signal_name} {signal_type} {signal_payload} ********")
            # start to dispatch order
            if signal_name == 'LOAD_DISPATCH' and signal_type == 'level':
                if signal_payload:
                    pass
                    await handle_dispatch(
                        device_settings=device_settings,
                        device_type=device_type,
                        dispatch_quantity=signal_payload,
                        is_using_mock_device=is_using_mock_device,
                        emulated_device_api_url=emulated_device_api_url)

    except Exception as e:
        logging.error(f"Error pase event: {e}")
    return 'optIn'
