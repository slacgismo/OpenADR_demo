def parse_device_id_from_ven_id(ven_id: str) -> str:
    """
    Parse the ven_id to get the device_id
    """
    return ven_id.split("-")[1]
