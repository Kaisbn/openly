from openly.devices.switch import Switch
from openly.exceptions import InvalidParametersError


class Lock(Switch):
    modes = ["locked", "unlocked"]

    def lock(self) -> None:
        self.mode = "locked"

    def unlock(self) -> None:
        self.mode = "unlocked"

    @property
    def cmd(self) -> dict:
        return {"mode": "unlock" if self.mode == "unlocked" else "lock"}

    @property
    def battery(self) -> int:
        return self.status.get("battery", 0)

    @property
    def mode(self) -> str | None:
        if not hasattr(self, "status") or "mode" not in self.status:
            return None
        return self.status["mode"].get("type", "locked")

    @mode.setter
    def mode(self, mode: dict | str) -> None:
        if isinstance(mode, dict):
            if "type" not in mode:
                raise InvalidParametersError("Invalid mode")
            mode = str(mode.get("type"))

        if mode not in self.modes:
            raise InvalidParametersError("Invalid mode")

        self.status["mode"]["type"] = mode
