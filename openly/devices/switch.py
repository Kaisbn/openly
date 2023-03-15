from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class Switch(BaseDevice):
    modes = ["off", "on"]

    mode: str = "off"  # Default mode

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if self.status and "mode" in self.status:
            if self.status["mode"] not in self.modes:
                raise InvalidParametersError("Invalid mode")
            self.mode = self.status["mode"]
        else:
            raise InvalidParametersError("Invalid status")

    def on(self):
        self.mode = "on"

    def off(self):
        self.mode = "off"

    @property
    def cmd(self) -> dict:
        return {"mode": self.mode}
