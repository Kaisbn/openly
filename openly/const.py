"""Constants for the Rently integration."""
from openly.devices.dimmer import Dimmer
from openly.devices.hub import Hub
from openly.devices.leak import LeakSensor
from openly.devices.lock import Lock
from openly.devices.switch import Switch
from openly.devices.thermostat import Thermostat

# Supported devices
DEVICES = {
    "dimmable_switch": Dimmer,
    "hub": Hub,
    "leakage_sensor": LeakSensor,
    "lock": Lock,
    "thermostat": Thermostat,
    "switch": Switch,
}

HEADER_KEY_AUTHORIZATION = "Authorization"
HEADER_KEY_USER_AGENT = "User-Agent"
HEADER_KEY_CONTENT_TYPE = "Content-Type"

HEADER_VALUE_USER_AGENT = "keyless/1102 CFNetwork/1220.1 Darwin/20.3.0"
HEADER_VALUE_CONTENT_TYPE = "application/json"

API_DEFAULT_BASE_URL = "https://app2.keyless.rocks/api/"
API_RETRY_ATTEMPTS = 3
API_RETRY_TIME = 10  # seconds
