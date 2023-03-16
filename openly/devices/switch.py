from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class Switch(BaseDevice):
    modes = ["off", "on"]

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if hasattr(self, "status"):
            if not isinstance(self.status, dict) or "mode" not in self.status:
                raise InvalidParametersError("Invalid status")

            self.mode = self.status["mode"]

    def on(self):
        self.mode = "on"

    def off(self):
        self.mode = "off"

    @property
    def mode(self) -> str | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("mode", "off")

    @mode.setter
    def mode(self, mode: str) -> None:
        if mode not in self.modes:
            raise InvalidParametersError("Invalid mode")
        self.status["mode"] = mode

    @property
    def cmd(self) -> dict:
        return {"mode": self.mode}
