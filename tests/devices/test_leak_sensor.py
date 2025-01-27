import json
import unittest.mock as mock

import pytest

from openly.devices import LeakSensor
from openly.exceptions import InvalidParametersError


def test_leak_sensor_str_id(leaksensor_data):
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.id == leaksensor_data["id"]


def test_leak_sensor_int_id(leaksensor_data):
    leaksensor_data["id"] = 123
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.id == leaksensor_data["id"]


def test_leak_sensor_name(leaksensor_data):
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.name == leaksensor_data["device_name"]


def test_leak_sensor_name_none(leaksensor_data):
    del leaksensor_data["device_name"]
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    with pytest.raises(AttributeError):
        assert not leaksensor.name


def test_leak_sensor_battery(leaksensor_data):
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.battery == leaksensor_data["status"]["battery"]


def test_leak_sensor_battery_none(leaksensor_data):
    del leaksensor_data["status"]["battery"]
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.battery == 0


def test_leak_sensor_valid_mode(leaksensor_data):
    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )

    assert leaksensor.mode == leaksensor_data["status"]["leakage"]


def test_leak_sensor_invalid_mode(leaksensor_data):
    leaksensor_data["status"]["leakage"] = "invalid"

    with pytest.raises(InvalidParametersError):
        LeakSensor(device_id=leaksensor_data["id"], device_data=leaksensor_data)


def test_leak_sensor_status_none(leaksensor_data):
    del leaksensor_data["status"]

    leaksensor = LeakSensor(
        device_id=leaksensor_data["id"], device_data=leaksensor_data
    )
    assert not hasattr(leaksensor, "status")


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_leak_sensor(mock_request, cloud, leaksensor_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(leaksensor_data)
    mock_request.return_value.json.return_value = leaksensor_data

    result = cloud.get_device(leaksensor_data["id"])

    assert result
    assert isinstance(result, LeakSensor)

    assert result.id == leaksensor_data["id"]
