import json
import unittest.mock as mock

import pytest

from openly.devices import Dimmer
from openly.exceptions import InvalidParametersError


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_dimmer(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(switch_data)
    mock_request.return_value.json.return_value = switch_data

    result = cloud.get_device(switch_data["id"])

    assert result
    assert isinstance(result, Dimmer)

    assert result.id == switch_data["id"]


def test_dimmer_str_id(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    assert dimmer.id == switch_data["id"]


def test_dimmer_int_id(switch_data):
    switch_data["id"] = 123
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    assert dimmer.id == switch_data["id"]


def test_dimmer_name(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    assert dimmer.name == switch_data["device_name"]


def test_dimmer_name_none(switch_data):
    del switch_data["device_name"]
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    with pytest.raises(AttributeError):
        assert not dimmer.name


def test_dimmer_cmd_off(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    dimmer.off()

    assert dimmer.cmd == {"mode": "off", "power": 0}


def test_dimmer_cmd_on(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    dimmer.on()

    assert dimmer.cmd == {"mode": "on", "power": 100}


def test_dimmer_invalid_power(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    with pytest.raises(InvalidParametersError):
        dimmer.power = "invalid"


def test_dimmer_power_too_high(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)

    with pytest.raises(InvalidParametersError):
        dimmer.power = 101


def test_dimmer_power_up(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)
    cur_pow = dimmer.power
    dimmer.up(50)

    assert dimmer.cmd == {"mode": "on", "power": min(cur_pow + 50, 100)}


def test_dimmer_power_down(switch_data):
    dimmer = Dimmer(id=switch_data["id"], device_data=switch_data)
    cur_pow = dimmer.power
    dimmer.down(100)

    assert dimmer.cmd == {"mode": "off", "power": max(cur_pow - 100, 0)}


def test_dimmer_invalid_status(switch_data):
    switch_data["status"] = "invalid"
    with pytest.raises(InvalidParametersError):
        Dimmer(id=switch_data["id"], device_data=switch_data)
