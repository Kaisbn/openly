from openly.devices.switch import Switch
from openly.exceptions import InvalidParametersError

FAN_ON = "on"
FAN_AUTO = "auto"

HVAC_MODE_OFF = "off"
HVAC_MODE_HEAT = "heat"
HVAC_MODE_COOL = "cool"
HVAC_MODE_AUTO = "auto"


class Thermostat(Switch):
    modes = [HVAC_MODE_AUTO, HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_OFF]
    fan_modes = [FAN_AUTO, FAN_ON]

    def __init__(self, device_id: str | int, device_data: dict = {}) -> None:
        super().__init__(device_id, device_data)

        if hasattr(self, "status"):
            self.heating_setpoint = self.status.get("heating_setpoint")
            self.cooling_setpoint = self.status.get("cooling_setpoint")
            self.room_temp = self.status.get("room_temp")
        if hasattr(self, "settings"):
            self.fan_duration = self.settings.get("fan_on_time", 0)

    def auto(self) -> None:
        self.mode = HVAC_MODE_AUTO

    def heat(self) -> None:
        self.mode = HVAC_MODE_HEAT

    def cool(self):
        self.mode = HVAC_MODE_COOL

    @property
    def operating_state(self) -> str | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("operating_state")

    @property
    def heating_setpoint(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("heating_setpoint")

    @heating_setpoint.setter
    def heating_setpoint(self, temp: int | None) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        if temp < 50 or temp > 90:
            raise InvalidParametersError("Temperature must be between 50 and 90")
        if self.cooling_setpoint and self.cooling_setpoint - temp < 3:
            raise InvalidParametersError(
                "Heating setpoint must be at least 3 degrees lower thancooling setpoint"
            )
        self.status["heating_setpoint"] = temp

    @property
    def cooling_setpoint(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("cooling_setpoint")

    @cooling_setpoint.setter
    def cooling_setpoint(self, temp: int | None) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        if temp < 50 or temp > 90:
            raise InvalidParametersError("Temperature must be between 50 and 90")
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
    def room_temp(self, temp: int | None) -> None:
        if not temp or not isinstance(temp, int):
            raise InvalidParametersError("Invalid temperature")
        self.status["room_temp"] = int(temp)

    @property
    def fan(self) -> str:
        return self.status.get("fan", "auto")

    @fan.setter
    def fan(self, mode: str) -> None:
        if mode not in [FAN_AUTO, FAN_ON]:
            raise InvalidParametersError("Invalid fan mode")
        self.status["fan"] = mode

    @property
    def fan_duration(self) -> int | None:
        if not hasattr(self, "status"):
            return None
        return self.status.get("fan_duration") if self.fan == FAN_ON else None

    @fan_duration.setter
    def fan_duration(self, duration: int) -> None:
        # Duration is in minutes, 12 hours max
        if not isinstance(duration, int) or duration < 0 or duration > 720:
            raise InvalidParametersError("Invalid duration")
        if not duration:
            self.fan = FAN_AUTO
        self.status["fan_duration"] = duration or 0

    @property
    def battery(self) -> int:
        return self.status.get("battery", 0)

    @battery.setter
    def battery(self, level: int) -> None:
        if not isinstance(level, int) or level < 0 or level > 100:
            raise InvalidParametersError("Invalid battery level")
        self.status["battery"] = level

    @property
    def cmd(self) -> dict:
        return {
            "commands": {
                "mode": self.mode,
                "heating_setpoint": self.heating_setpoint,
                "cooling_setpoint": self.cooling_setpoint,
                "fan": self.fan,
            },
            "settings": {"fan_on_mode": self.fan_duration},
        }
