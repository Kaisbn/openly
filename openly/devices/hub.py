from openly.devices.base_device import BaseDevice


class Hub(BaseDevice):
    home_name: str

    @property
    def name(self) -> str:
        return self.home_name
