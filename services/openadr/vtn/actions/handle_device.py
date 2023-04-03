
import logging


async def check_device_id_from_tess_device_api(
    ven_id: str,
    agent_id: str,
    resource_id: str,
    DEVICES_API_URL: str,
):
    logging.info(
        "Check device id , agent_id and resource id from tess device api")
