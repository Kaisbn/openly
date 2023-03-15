from openly.devices.switch import Switch
from openly.exceptions import InvalidParametersError


class Dimmer(Switch):
    power: int = 0  # Default power

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if self.status and "power" in self.status:
            if not self.status["power"].isdigit():
                raise InvalidParametersError("Invalid power")
            self.power = self.status["power"]
        else:
            raise InvalidParametersError("Invalid status")

    def on(self):
        super().on()
        self.power = 100

    def off(self):
        super().off()
        self.power = 0

    def up(self, step=10):
        self.power = min(self.power + step, 100)

    def down(self, step=10):
        self.power = max(self.power - step, 0)

    @property
    def cmd(self):
        return {"mode": self.mode, "power": self.power}
