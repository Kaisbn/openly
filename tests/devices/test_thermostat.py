import json
import unittest.mock as mock

import pytest

from openly.devices import Thermostat
from openly.exceptions import InvalidParametersError


def test_thermostat_str_id(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.id == thermostat_data["id"]


def test_thermostat_int_id(thermostat_data):
    thermostat_data["id"] = 123
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.id == thermostat_data["id"]


def test_thermostat_name(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.name == thermostat_data["device_name"]


def test_thermostat_name_none(thermostat_data):
    del thermostat_data["device_name"]
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    with pytest.raises(AttributeError):
        assert not thermostat.name


def test_thermostat_cmd(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.cmd["commands"] == {
        "mode": thermostat_data["status"]["mode"],
        "fan": thermostat_data["status"]["fan"],
        "heating_setpoint": thermostat_data["status"]["heating_setpoint"],
        "cooling_setpoint": thermostat_data["status"]["cooling_setpoint"],
    }


def test_thermostat_auto(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    thermostat.auto()

    assert thermostat.mode == "auto"


def test_thermostat_cool(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    thermostat.cool()

    assert thermostat.mode == "cool"


def test_thermostat_heat(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    thermostat.heat()

    assert thermostat.mode == "heat"


def test_thermostat_off(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    thermostat.off()

    assert thermostat.mode == "off"


def test_thermostat_battery(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.battery == thermostat_data["status"]["battery"]


def test_thermostat_battery_none(thermostat_data):
    del thermostat_data["status"]["battery"]
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.battery == 0


def test_thermostat_mode(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.mode == thermostat_data["status"]["mode"]


def test_thermostat_mode_none(thermostat_data):
    del thermostat_data["status"]["mode"]

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_mode_invalid(thermostat_data):
    thermostat_data["status"]["mode"] = "invalid"

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_mode_no_type(thermostat_data):
    del thermostat_data["status"]["mode"]

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_heating_setpoint(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert (
        thermostat.heating_setpoint
        == thermostat_data["status"]["heating_setpoint"]
    )


def test_thermostat_heating_setpoint_none(thermostat_data):
    del thermostat_data["status"]["heating_setpoint"]

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_heating_setpoint_too_low(thermostat_data):
    thermostat_data["status"]["heating_setpoint"] = 40

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_heating_setpoint_too_high(thermostat_data):
    thermostat_data["status"]["heating_setpoint"] = 100

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_heating_setpoint_too_close(thermostat_data):
    thermostat_data["status"]["heating_setpoint"] = (
        thermostat_data["status"]["cooling_setpoint"] - 2
    )

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_cooling_setpoint(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert (
        thermostat.cooling_setpoint
        == thermostat_data["status"]["cooling_setpoint"]
    )


def test_thermostat_cooling_setpoint_none(thermostat_data):
    del thermostat_data["status"]["cooling_setpoint"]

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_cooling_setpoint_too_low(thermostat_data):
    thermostat_data["status"]["cooling_setpoint"] = 40

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_cooling_setpoint_too_high(thermostat_data):
    thermostat_data["status"]["cooling_setpoint"] = 100

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_cooling_setpoint_too_close(thermostat_data):
    thermostat_data["status"]["cooling_setpoint"] = (
        thermostat_data["status"]["heating_setpoint"] + 1
    )

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


def test_thermostat_room_temp(thermostat_data):
    thermostat = Thermostat(
        device_id=thermostat_data["id"], device_data=thermostat_data
    )

    assert thermostat.room_temp == thermostat_data["status"]["room_temp"]


def test_thermostat_room_temp_none(thermostat_data):
    del thermostat_data["status"]["room_temp"]

    with pytest.raises(InvalidParametersError):
        Thermostat(device_id=thermostat_data["id"], device_data=thermostat_data)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_thermostat(mock_request, cloud, thermostat_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(thermostat_data)
    mock_request.return_value.json.return_value = thermostat_data

    result = cloud.get_device(thermostat_data["id"])

    assert result
    assert isinstance(result, Thermostat)

    assert result.id == thermostat_data["id"]
