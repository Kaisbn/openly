from abc import ABC, abstractproperty


class BaseDevice(ABC):
    """
    Base abstract class for Rently supported devices
    """
    _id: str = None

    def __init__(self, device_id: str = None, device_data: dict = None) -> None:
        self._id = device_id
        self._data = device_data

    def __str__(self) -> str:
        return f"{type(self).__name__} - {self._id}"

    @property
    def device_id(self) -> str:
        return self._id or self._data["id"]

    @property
    def name(self) -> str:
        return self._data["device_name"]

    @abstractproperty
    def cmd(self) -> dict[str, any]:
        return {}
