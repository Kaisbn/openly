from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class LeakSensor(BaseDevice):
    modes = ["yes", "no"]

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if self.status and "leakage" in self.status:
            if self.status["leakage"] not in self.modes:
                raise InvalidParametersError("Invalid mode")
            self.mode = self.status["leakage"]
        else:
            raise InvalidParametersError("Invalid status")
