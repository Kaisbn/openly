from openly.devices.switch import Switch
from openly.exceptions import InvalidParametersError


class Dimmer(Switch):
    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if hasattr(self, "status"):
            self.power = self.status.get("power", 0)

    def up(self, step=10):
        self.power = min(self.power + step, 100)

        if self.power > 0:
            self.on()

    def down(self, step=10):
        self.power = max(self.power - step, 0)

        if self.power == 0:
            self.off()

    @property
    def power(self):
        return self.status.get("power", 0)

    @power.setter
    def power(self, power):
        if not isinstance(power, int) and not power.isdigit():
            raise InvalidParametersError("Invalid power")
        if power < 0 or power > 100:
            raise InvalidParametersError("Power must be between 0 and 100")
        self.status["power"] = power

    @property
    def cmd(self):
        return super().cmd | {"power": self.power}
