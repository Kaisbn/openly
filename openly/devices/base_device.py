from abc import ABC


class BaseDevice(ABC):
    """
    Base abstract class for Rently supported devices
    """

    _id: str | int
    device_name: str
    status: dict

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        self.__dict__.update(device_data)
        self.id = id

    def __str__(self) -> str:
        return f"{type(self).__name__} - {self._id}"

    @property
    def id(self) -> str | int:
        return self._id

    @id.setter
    def id(self, value: str | int) -> None:
        self._id = value

    @property
    def name(self) -> str:
        return self.device_name

    @property
    def cmd(self) -> dict:
        return {}
