import logging

from .handle_device import check_device_id_from_tess_device_api


async def on_create_party_registration(registration_info, VENS, DEVICES_API_URL):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """

    ven_name = registration_info['ven_name']
    for v in VENS.values():
        # print(values['ven_name'])
        if v.get('ven_name') == ven_name:
            logging.debug(
                f"REGISTRATION SUCCESS WITH NAME:  {v.get('ven_name')} FROM PAYLOAD, MATCH FOUND {ven_name}")
            return v['ven_id'], v['registration_id']
        else:
            response = await check_device_id_from_tess_device_api(
                ven_id=VENS['ven_id'],
                agent_id=VENS['agent_id'],
                resource_id=VENS['resource_id'],
                DEVICES_API_URL=DEVICES_API_URL
            logging.debug(
                f"REGISTRATION FAIL BAD VEN NAME: {registration_info['ven_name']}")
            return False
