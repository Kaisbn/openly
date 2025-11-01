import json
import unittest.mock as mock

import pytest

from openly.devices import Dimmer
from openly.exceptions import InvalidParametersError


def test_dimmer_str_id(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    assert dimmer.id == switch_data["id"]


def test_dimmer_int_id(switch_data):
    data_copy = switch_data.copy()
    data_copy["id"] = 123
    dimmer = Dimmer(device_id=switch_data["id"], device_data=data_copy)

    assert dimmer.device_id == switch_data["id"]


def test_dimmer_name(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    assert dimmer.name == switch_data["device_name"]


def test_dimmer_name_none(switch_data):
    data_copy = switch_data.copy()
    del data_copy["device_name"]
    dimmer = Dimmer(device_id=switch_data["id"], device_data=data_copy)

    with pytest.raises(AttributeError):
        assert not dimmer.name


def test_dimmer_cmd_off(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    dimmer.off()

    assert dimmer.cmd == {
        "commands": {
            "mode": "off",
            "power": switch_data["status"]["power"],
        }
    }


def test_dimmer_cmd_on(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    dimmer.on()

    assert dimmer.cmd == {
        "commands": {
            "mode": "on",
            "power": switch_data["status"]["power"],
        }
    }


def test_dimmer_invalid_power(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    with pytest.raises(InvalidParametersError):
        dimmer.power = "invalid"


def test_dimmer_power_too_high(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    with pytest.raises(InvalidParametersError):
        dimmer.power = 101


def test_dimmer_power_up(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)
    cur_pow = dimmer.power
    dimmer.up(50)

    assert dimmer.cmd == {"commands": {"mode": "on", "power": min(cur_pow + 50, 100)}}


def test_dimmer_power_down(switch_data):
    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)
    cur_pow = dimmer.power
    dimmer.down(50)

    assert dimmer.cmd == {"commands": {"mode": "off", "power": max(cur_pow - 50, 0)}}


def test_dimmer_status_none(switch_data):
    del switch_data["status"]

    dimmer = Dimmer(device_id=switch_data["id"], device_data=switch_data)

    assert not hasattr(dimmer, "status")


def test_dimmer_status_empty(switch_data):
    switch_data["status"] = {}

    with pytest.raises(InvalidParametersError):
        Dimmer(device_id=switch_data["id"], device_data=switch_data)


def test_dimmer_status_invalid(switch_data):
    switch_data["status"] = "invalid"

    with pytest.raises(InvalidParametersError):
        Dimmer(device_id=switch_data["id"], device_data=switch_data)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_dimmer(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(switch_data)
    mock_request.return_value.json.return_value = switch_data

    result = cloud.get_device(switch_data["id"])

    assert result
    assert isinstance(result, Dimmer)

    assert result.id == switch_data["id"]
