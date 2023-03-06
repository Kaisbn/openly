"""Constants for the Rently integration."""
from openly.devices.hub import Hub
from openly.devices.leak import LeakSensor
from openly.devices.lock import Lock
from openly.devices.switch import Dimmer
from openly.devices.thermostat import Thermostat

# Supported devices
DEVICES = {
    "dimmable_switch": Dimmer,
    "hub": Hub,
    "leakage_sensor": LeakSensor,
    "lock": Lock,
    "thermostat": Thermostat,
}

HEADER_KEY_AUTHORIZATION = "Authorization"
HEADER_KEY_USER_AGENT = "User-Agent"
HEADER_KEY_CONTENT_TYPE = "Content-Type"

HEADER_VALUE_USER_AGENT = "keyless/1102 CFNetwork/1220.1 Darwin/20.3.0"
HEADER_VALUE_CONTENT_TYPE = "application/json"

API_RETRY_ATTEMPTS = 3
API_RETRY_TIME = 10 # seconds
