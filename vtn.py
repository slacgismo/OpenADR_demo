import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial
from openleadr.objects import Target, Interval
enable_default_logging()


async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    if registration_info['ven_name'] == 'ven123':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        return ven_id, registration_id
    else:
        return False


async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    callback = partial(on_update_report, ven_id=ven_id,
                       resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval


async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    for time, value in data:
        print("-----------------------1------------------")
        print(
            f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")


async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    print("-----------------------2------------------")
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")


async def event_callback(ven_id, event_id, opt_status, opt_type):
    print("-----------------------3------------------")
    print(
        f"VEN {ven_id} responded {opt_status} to event {event_id} opt_type {opt_type}")


# Create the server object
server = OpenADRServer(vtn_id='myvtn')

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration',
                   on_create_party_registration)

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
event_id = server.add_event(ven_id='ven_id_123',
                            signal_name='simple',
                            signal_type='level',
                            intervals=[{'dtstart': datetime(2022, 12, 15, 12, 0, 0, tzinfo=timezone.utc),
                                        'duration': timedelta(minutes=10),
                                        'signal_payload': 1}],
                            target=Target(resource_id='device001'),
                            callback=event_callback)
print(f"event_id {event_id}")
# event_id = server.add_event(ven_id='ven123',
#                             signal_name='simple',
#                             signal_type='level',
#                             intervals=[{'dtstart': datetime(2022, 12, 15, 12, 0, 0, tzinfo=timezone.utc),
#                                         'duration': timedelta(minutes=10),
#                                         'signal_payload': 1}],
#                             target=[{'resource_id': 'Device001'}],
#                             callback=event_callback)

# Run the server on the asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()
