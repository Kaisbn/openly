from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError, MissingParametersError


class Thermostat(BaseDevice):
    modes = ["auto", "cool", "heat", "off"]

    mode: str = "off"  # Default mode
    heat_celsius: int = 0  # Default heat
    cool_celsius: int = 0  # Default cool
    temp_celsius: int = 0  # Default temp

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if self.status and "mode" in self.status:
            if self.status["mode"] not in self.modes:
                raise InvalidParametersError("Invalid mode")
            self.mode = self.status["mode"]

            if "heating_setpoint" not in self.status:
                raise InvalidParametersError("Invalid heating temperature")
            self.heat_celsius = self.status["heating_setpoint"]

            if "cooling_setpoint" not in self.status:
                raise InvalidParametersError("Invalid cooling temperature")
            self.cool_celsius = self.status["cooling_setpoint"]

            if "room_temp" not in self.status:
                raise InvalidParametersError("Invalid room temperature")
            self.temp_celsius = self.status["room_temp"]
        else:
            raise InvalidParametersError("Invalid status")

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
    def cmd(self) -> dict:
        cmd = {
            "mode": self.mode,
            "heating_setpoint": self.heat_celsius,
            "cooling_setpoint": self.cool_celsius,
        }

        if not all(cmd.values()):
            raise MissingParametersError("Missing data to generate command")

        return cmd
