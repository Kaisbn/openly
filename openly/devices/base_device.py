from abc import ABC


class BaseDevice(ABC):
    """
    Base abstract class for Rently supported devices
    """

    _device_id: str | int
    device_name: str
    status: dict

    def __init__(self, device_id: str | int, device_data: dict = {}) -> None:
        self.__dict__.update(device_data)
        self.device_id = device_id

    def __str__(self) -> str:
        return f"{type(self).__name__} - {self._device_id}"

    @property
    def device_id(self) -> str | int:
        return self._device_id

    @device_id.setter
    def device_id(self, value: str | int) -> None:
        self._device_id = value

    @property
    def name(self) -> str:
        return self.device_name

    @property
    def cmd(self) -> dict:
        return {}
