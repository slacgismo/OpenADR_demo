class SharedDeviceData:
    """
    This is a singleton class that is used to share data between the different threads.

    """
    __instance = None

    def __init__(self, initial_value=None):
        if SharedDeviceData.__instance is not None:
            raise Exception(
                "Cannot create multiple instances of SharedDeviceData, use get_instance()")
        self._value = initial_value
        SharedDeviceData.__instance = self

    @staticmethod
    def get_instance(initial_value=None):
        if SharedDeviceData.__instance is None:
            SharedDeviceData(initial_value)
        return SharedDeviceData.__instance

    def get(self):
        return self._value

    def set(self, new_value):
        self._value = new_value
