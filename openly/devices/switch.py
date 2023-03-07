from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class Switch(BaseDevice):
    modes = ["off", "on"]

    mode: str = None

    def __init__(
        self, device_id: str = None, device_data: dict = None
    ) -> None:
        super().__init__(device_id, device_data)

        if "status" in self._data:
            self.mode = self._data["status"]["mode"]
            if self.mode not in self.modes:
                raise InvalidParametersError("Invalid mode")

    def on(self):
        self.mode = "on"

    def off(self):
        self.mode = "off"

    @property
    def cmd(self):
        return {"mode": self.mode}
