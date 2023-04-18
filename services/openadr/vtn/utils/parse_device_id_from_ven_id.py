def parse_device_id_from_ven_id(ven_id: str) -> str:
    """
    Parse the ven_id to get the device_id
    """
    split_string = ven_id.split("-")
    if len(split_string) == 2:
        return split_string[1]
    else:
        raise Exception(f"Error parse ven_id: {ven_id}")
