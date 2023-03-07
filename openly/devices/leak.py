from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class LeakSensor(BaseDevice):
    modes = ["yes", "no"]

    mode: str = None

    def __init__(
        self, device_id: str = None, device_data: dict = None
    ) -> None:
        super().__init__(device_id, device_data)

        if "status" in self._data:
            self.mode = self._data["status"]["leakage"]
            if self.mode not in self.modes:
                raise InvalidParametersError("Invalid mode")

    @property
    def cmd(self):
        return {}
