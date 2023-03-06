from openly.devices.switch import Switch


class Dimmer(Switch):
    power: int = None

    def __init__(self, device_id: str = None, device_data: dict = None) -> None:
        super().__init__(device_id, device_data)

        if "status" in self._data:
            self.power = self._data["status"]["power"]

    def off(self):
        self.mode = "off"
        self.power = 0

    def up(self, step=10):
        self.power = min(self.power + step, 100)

    def down(self, step=10):
        self.power = max(self.power - step, 0)

    @property
    def cmd(self):
        return {"mode": self.mode, "power": self.power}
