# class VENDict:
#     def __init__(self):
#         self.VENs = dict()

#     def add_ven(self, ven_id: str, device_id: str):
#         self.VENs[ven_id] = {
#             'device_id': device_id,
#         }

#     def get_ven(self, ven_id: str):
#         return self.VENs.get(ven_id)

#     def remove_ven(self, ven_id: str):
#         self.VENs.pop(ven_id, None)

#     def check_ven(self, ven_id: str):
#         return ven_id in self.VENs

#     def number_of_vens(self):
#         if self.VENs is None:
#             return 0
#         else:
#             return len(self.VENs)


class SharedVenInfos:
    """
    This is a singleton class that is used to share data between different threads.
    """

    __instance = None

    def __init__(self,

                 resource_id: str = None,
                 agent_id: str = None,
                 vtn_id: str = None,
                 VENs: dict = None,
                 market_interval_in_seconds: int = None,
                 is_using_mock_device: bool = None,
                 emulated_device_api_url: str = None

                 ):
        if SharedVenInfos.__instance is not None:
            raise Exception(
                "Cannot create multiple instances of SharedDeviceInfo, use get_instance() instead")
        self._resource_id = resource_id
        self._agent_id = agent_id
        self._VENs = VENs
        self._vtn_id = vtn_id
        self._is_using_mock_device = is_using_mock_device
        self._market_interval_in_seconds = market_interval_in_seconds
        self._emulated_device_api_url = emulated_device_api_url
        SharedVenInfos.__instance = self

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = SharedVenInfos()
        return cls.__instance

    def get_vtn_id(self):
        return self._vtn_id

    def set_vtn_id(self, vtn_id):
        self._vtn_id = vtn_id

    def get_resource_id(self):
        return self._resource_id

    def set_resource_id(self, resource_id):
        self._resource_id = resource_id

    def get_agent_id(self):
        return self._agent_id

    def set_anget_id(self, agent_id):
        self._agent_id = agent_id

    def get_is_using_mock_device(self):
        return self._is_using_mock_device

    def set_is_using_mock_device(self, is_using_mock_device):
        self._is_using_mock_device = is_using_mock_device

    def get_emulated_device_api_url(self):
        return self._emulated_device_api_url

    def set_emulated_device_api_url(self, emulated_device_api_url):
        self._emulated_device_api_url = emulated_device_api_url

    def get_vens(self):
        return self._VENs

    def set_vens(self, VENs):
        self._VENs = VENs

    def add_ven(self, ven_id: str, device_id: str = None, ven_name: str = None, registration_id: str = None):
        if self._VENs is None:
            self._VENs = dict()
        else:
            self._VENs[ven_id] = {
                "device_id": device_id,
                "ven_name": ven_name,
                "registration_id": registration_id
            }

    def get_ven_from_ven_id(self, ven_id: str):
        return self._VENs.get(ven_id)

    def get_registration_id_from_ven_id(self, ven_id: str):
        return self._VENs.get(ven_id).get("registration_id")

    def remove_ven(self, ven_id: str):
        self._VENs.pop(ven_id, None)

    def check_ven(self, ven_id: str):
        return ven_id in self._VENs

    def number_of_vens(self):
        if self._VENs is None:
            return 0
        else:
            return len(self._VENs)

    def get_market_interval_in_seconds(self):
        return self._market_interval_in_seconds

    def set_market_interval_in_seconds(self, market_interval_in_seconds):
        self._market_interval_in_seconds = market_interval_in_seconds
