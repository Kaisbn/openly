from openly.devices.switch import Switch
from openly.exceptions import InvalidParametersError


class Thermostat(Switch):
    modes = ["auto", "cool", "heat", "off"]
    fan_modes = ["auto", "on"]

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if hasattr(self, "status"):
            self.heating_setpoint = self.status.get("heating_setpoint", None)
            self.cooling_setpoint = self.status.get("cooling_setpoint", None)
            self.room_temp = self.status.get("room_temp", None)

    def auto(self) -> None:
        self.mode = "auto"

    def heat(self) -> None:
        self.mode = "heat"

    def cool(self):
        self.mode = "cool"

    @property
    def heating_setpoint(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("heating_setpoint")

    @heating_setpoint.setter
    def heating_setpoint(self, temp: int) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        if temp < 50 or temp > 90:
            raise InvalidParametersError(
                "Temperature must be between 50 and 90"
            )
        if self.cooling_setpoint and self.cooling_setpoint - temp < 3:
            raise InvalidParametersError(
                "Heating setpoint must be at least 3 degrees lower than"
                "cooling setpoint"
            )
        self.status["heating_setpoint"] = temp

    @property
    def cooling_setpoint(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("cooling_setpoint")

    @cooling_setpoint.setter
    def cooling_setpoint(self, temp: int) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        if temp < 50 or temp > 90:
            raise InvalidParametersError(
                "Temperature must be between 50 and 90"
            )
        if self.heating_setpoint and temp - self.heating_setpoint < 3:
            raise InvalidParametersError(
                "Cooling setpoint must be at least 3 degrees higher than"
                "heating setpoint"
            )
        self.status["cooling_setpoint"] = temp

    @property
    def room_temp(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("room_temp")

    @room_temp.setter
    def room_temp(self, temp: int) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        self.status["room_temp"] = int(temp)

    @property
    def fan(self) -> str:
        return self.status.get("fan", "auto")

    @property
    def battery(self) -> int:
        return self.status.get("battery", 0)

    @property
    def cmd(self) -> dict:
        return super().cmd | {
            "fan": self.fan,
            "heating_setpoint": self.heating_setpoint,
            "cooling_setpoint": self.cooling_setpoint,
        }
