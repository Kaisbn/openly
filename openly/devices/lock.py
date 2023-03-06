from openly.devices.base_device import BaseDevice
from openly.exceptions import InvalidParametersError


class Lock(BaseDevice):
    modes = ["lock", "unlock"]

    mode: str = None

    def __init__(self, device_id: str = None, device_data: dict = None) -> None:
        super().__init__(device_id, device_data)

        if "status" in self._data:
            cur_mode = self._data["status"]["mode"]["type"]
            if cur_mode == "locked":
                self.mode = "lock"
            elif cur_mode == "unlocked":
                self.mode = "unlock"
            else:
                raise InvalidParametersError("Invalid mode")

    def lock(self) -> None:
        self.mode = "lock"

    def unlock(self) -> None:
        self.mode = "unlock"

    @property
    def cmd(self) -> dict[str, any]:
        return {"mode": self.mode}

    @property
    def status(self) -> str:
        return self._data["status"]["mode"]["type"]

    @property
    def battery(self) -> int:
        return self._data["status"]["mode"]["battery"]
