from models_classes.SharedDeviceInfo import SharedDeviceInfo


def setup_global_variables(
        shared_device_info: SharedDeviceInfo,
        device_settings: dict,
        flexible: bool,
        device_id: str,
        meter_id: str,
        resource_id: str,
        ven_id: str,
        agent_id: str,
        device_type: str,
        emulated_device_api_url: str,
        is_using_mock_device: bool,
        market_interval_in_seconds: int,
        market_start_time: str,


):
    shared_device_info.set_device_id(device_id)
    shared_device_info.set_meter_id(meter_id)
    shared_device_info.set_resource_id(resource_id)
    shared_device_info.set_ven_id(ven_id)
    shared_device_info.set_agent_id(agent_id)
    shared_device_info.set_flxible(int(flexible))
    shared_device_info.set_device_settings(device_settings)
    shared_device_info.set_device_type(device_type)
    shared_device_info.set_emulated_device_api_url(emulated_device_api_url)
    shared_device_info.set_is_using_mock_device(is_using_mock_device)
    shared_device_info.set_market_interval(market_interval_in_seconds)
    shared_device_info.set_market_start_time(market_start_time)
    return None
