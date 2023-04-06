class SharedDeviceInfo:
    """
    This is a singleton class that is used to share data between different threads.
    """

    __instance = None
    # is_using_mock_device = shared_device_info.get('is_using_mock_device')
    # emulated_device_api_url = shared_device_info.get(
    #     'emulated_device_api_url')

    def __init__(self,
                 device_id: str = None,
                 resource_id: str = None,
                 meter_id: str = None,
                 flexible: str = None,
                 agent_id: str = None,
                 ven_id: str = None,
                 device_settings: dict = None,
                 device_type: str = None,
                 is_using_mock_device: bool = None,
                 emulated_device_api_url: str = None,
                 market_interval: int = None,
                 dispatch_queue: list = None,
                 market_start_time: str = None,
                 #  dispatch_timestamp: int = None,
                 #  dispatch_quantity: float = None,
                 #  price: float = None,
                 #  order_id: str = None,
                 ):
        if SharedDeviceInfo.__instance is not None:
            raise Exception(
                "Cannot create multiple instances of SharedDeviceInfo, use get_instance() instead")
        self._device_id = device_id
        self._resource_id = resource_id
        self._meter_id = meter_id
        self._flexible = flexible
        self._agent_id = agent_id
        self._device_settings = device_settings
        self._device_type = device_type
        self._ven_id = ven_id
        self._is_using_mock_device = is_using_mock_device
        self._emulated_device_api_url = emulated_device_api_url
        self._market_start_time = market_start_time

        self._market_interval = market_interval
        self._dispatch_queue = dispatch_queue
        # self._dispatch_timestamp = dispatch_timestamp
        # self._dispatch_quantity = dispatch_quantity
        # self._price = price
        # self._order_id = order_id

        SharedDeviceInfo.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = SharedDeviceInfo()
        return cls.__instance

    def get_device_id(self):
        return self._device_id

    def set_device_id(self, device_id):
        self._device_id = device_id

    def get_resource_id(self):
        return self._resource_id

    def set_resource_id(self, resource_id):
        self._resource_id = resource_id

    def get_meter_id(self):
        return self._meter_id

    def set_meter_id(self, meter_id):
        self._meter_id = meter_id

    def get_flexible(self):
        return self._flexible

    def set_flxible(self, flexible):
        self._flexible = flexible

    def get_agent_id(self):
        return self._agent_id

    def set_agent_id(self, agent_id):
        self._agent_id = agent_id

    def get_ven_id(self):
        return self._ven_id

    def set_ven_id(self, ven_id):
        self._ven_id = ven_id

    def get_device_settings(self):
        return self._device_setting

    def set_device_settings(self, device_setting):
        self._device_setting = device_setting

    def get_device_type(self):
        return self._device_type

    def set_device_type(self, device_type):
        self._device_type = device_type

    def get_is_using_mock_device(self):
        return self._is_using_mock_device

    def set_is_using_mock_device(self, is_using_mock_device):
        self._is_using_mock_device = is_using_mock_device

    def get_emulated_device_api_url(self):
        return self._emulated_device_api_url

    def set_emulated_device_api_url(self, emulated_device_api_url):
        self._emulated_device_api_url = emulated_device_api_url

    def get_market_interval(self):
        return self._market_interval

    def set_market_interval(self, market_interval):
        self._market_interval = market_interval

    def get_first_dispatch(self):
        if self._dispatch_queue is not None and len(self._dispatch_queue) > 0:
            return self._dispatch_queue.pop(0)
        else:
            return None

    def len_dispatch_queue(self):
        return len(self._dispatch_queue)

    def set_dispatch_queue(self,
                           order_id: str = None,
                           dispatch_timestamp: int = None,
                           quantity: float = None,
                           price: float = None,
                           ):
        if self._dispatch_queue is None:
            self._dispatch_queue = []

        self._dispatch_queue.append({
            'order_id': order_id,
            'dispatch_timestamp': dispatch_timestamp,
            'quantity': quantity,
            'price': price,
        })

    def get_market_start_time(self):
        return self._market_start_time

    def set_market_start_time(self, market_start_time):
        self._market_start_time = market_start_time
