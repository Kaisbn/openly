from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError, MissingParametersError


class Thermostat(BaseDevice):
    modes = ["auto", "cool", "heat", "off"]

    mode: str = None
    heat_celsius: int = None
    cool_celsius: int = None
    temp_celsius: int = None

    def __init__(
        self, device_id: str = None, device_data: dict = None
    ) -> None:
        super().__init__(device_id, device_data)

        if "status" in self._data:
            self.mode = self._data["status"]["mode"]
            if self.mode not in self.modes:
                raise InvalidParametersError("Invalid mode")

            self.heat_celsius = self._data["status"]["heating_setpoint"]
            self.cool_celsius = self._data["status"]["cooling_setpoint"]
            self.temp_celsius = self._data["status"]["room_temp"]

    def off(self):
        self.mode = "off"

    def auto(self):
        self.mode = "auto"

    def heat(self):
        self.mode = "heat"

    def cool(self):
        self.mode = "cool"

    def high(self, temp=70):
        self.cool_celsius = temp

    def low(self, temp=70):
        self.heat_celsius = temp

    @property
    def cmd(self):
        cmd = {
            "mode": self.mode,
            "heating_setpoint": self.heat_celsius,
            "cooling_setpoint": self.cool_celsius,
        }

        if not all(cmd.values()):
            raise MissingParametersError("Missing data to generate command")

        return cmd
