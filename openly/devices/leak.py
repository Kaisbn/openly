from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class LeakSensor(BaseDevice):
    modes = ["yes", "no"]

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if hasattr(self, "status"):
            self.mode = self.status.get("leakage", "no")

    @property
    def battery(self) -> int:
        return self.status.get("battery", 0)

    @property
    def mode(self) -> str:
        return self.status.get("leakage", "no")

    @mode.setter
    def mode(self, mode: str) -> None:
        if mode not in self.modes:
            raise InvalidParametersError("Invalid mode")
        self.status["leakage"] = mode
