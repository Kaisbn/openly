from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class Lock(BaseDevice):
    modes = ["lock", "unlock"]

    mode: str = "lock"  # Default mode

    def __init__(self, id: str | int, device_data: dict = {}) -> None:
        super().__init__(id, device_data)

        if (
            self.status
            and "mode" in self.status
            and "type" in self.status["mode"]
        ):
            cur_mode = self.status["mode"]["type"]
            if cur_mode == "locked":
                self.mode = "lock"
            elif cur_mode == "unlocked":
                self.mode = "unlock"
            else:
                raise InvalidParametersError("Invalid mode")
        else:
            raise InvalidParametersError("Invalid status")

    def lock(self) -> None:
        self.mode = "lock"

    def unlock(self) -> None:
        self.mode = "unlock"

    @property
    def cmd(self) -> dict:
        return {"mode": self.mode}

    @property
    def type(self) -> str:
        return self.status["mode"]["type"]

    @property
    def battery(self) -> int:
        return self.status["mode"]["battery"]
