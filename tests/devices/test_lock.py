import json
import unittest.mock as mock

import pytest

from openly.devices import Lock
from openly.exceptions import InvalidParametersError


def test_lock_str_id(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.id == lock_data["id"]


def test_lock_int_id(lock_data):
    lock_data["id"] = 123
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.id == lock_data["id"]


def test_lock_name(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.name == lock_data["device_name"]


def test_lock_name_none(lock_data):
    del lock_data["device_name"]
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    with pytest.raises(AttributeError):
        assert not lock.name


def test_lock_cmd(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.cmd == {"mode": "lock"}


def test_lock_lock(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    lock.lock()

    assert lock.cmd == {"mode": "lock"}
    assert lock.mode == "locked"


def test_lock_unlock(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    lock.unlock()

    assert lock.cmd == {"mode": "unlock"}
    assert lock.mode == "unlocked"


def test_lock_battery(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.battery == lock_data["status"]["battery"]


def test_lock_battery_none(lock_data):
    del lock_data["status"]["battery"]
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.battery == 0


def test_lock_mode(lock_data):
    lock = Lock(id=lock_data["id"], device_data=lock_data)

    assert lock.mode == lock_data["status"]["mode"]["type"]


def test_lock_mode_none(lock_data):
    del lock_data["status"]["mode"]

    with pytest.raises(InvalidParametersError):
        Lock(id=lock_data["id"], device_data=lock_data)


def test_lock_mode_invalid(lock_data):
    lock_data["status"]["mode"]["type"] = "invalid"

    with pytest.raises(InvalidParametersError):
        Lock(id=lock_data["id"], device_data=lock_data)


def test_lock_mode_no_type(lock_data):
    del lock_data["status"]["mode"]["type"]

    with pytest.raises(InvalidParametersError):
        Lock(id=lock_data["id"], device_data=lock_data)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_lock(mock_request, cloud, lock_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(lock_data)
    mock_request.return_value.json.return_value = lock_data

    result = cloud.get_device(lock_data["id"])

    assert result
    assert isinstance(result, Lock)

    assert result.id == lock_data["id"]
