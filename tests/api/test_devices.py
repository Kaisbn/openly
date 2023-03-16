import json
import unittest.mock as mock

import pytest

from openly.devices import Lock, Switch, Thermostat
from openly.exceptions import (
    InvalidResponseError,
    MissingParametersError,
    RentlyAuthError,
)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_devices(mock_request, cloud, devices_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(devices_data)
    mock_request.return_value.json.return_value = devices_data

    result = cloud.get_devices(hub_id=1)

    assert result
    assert isinstance(result, list)
    assert isinstance(result[0], Thermostat)
    assert isinstance(result[1], Lock)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_devices_offline(mock_request, cloud, devices_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    with pytest.raises(RentlyAuthError):
        cloud.get_devices(hub_id=1)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_devices_empty(mock_request, cloud):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = []
    mock_request.return_value.json.return_value = []

    with pytest.raises(InvalidResponseError):
        cloud.get_devices(hub_id=1)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_device(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(switch_data)
    mock_request.return_value.json.return_value = switch_data

    result = cloud.get_device(switch_data["id"])

    assert result
    assert isinstance(result, Switch)

    assert result.id == switch_data["id"]


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_device_offline(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    with pytest.raises(RentlyAuthError):
        cloud.get_device(switch_data["id"])


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_device_empty(mock_request, cloud):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = []
    mock_request.return_value.json.return_value = []

    with pytest.raises(InvalidResponseError):
        cloud.get_device(0)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_device_type_not_found(mock_request, cloud, switch_data):
    switch_data["device_type"] = "invalid"

    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(switch_data)
    mock_request.return_value.json.return_value = switch_data

    with pytest.raises(InvalidResponseError):
        cloud.get_device(switch_data["id"])


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_send_command(mock_request, cloud, switch_data):
    response = {"success": True, "message": "Success"}
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    cloud.send_command(switch_data["id"], {"mode": "on"})

    assert mock_request.called


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_send_command_offline(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    with pytest.raises(RentlyAuthError):
        cloud.send_command(switch_data["id"], {"mode": "on"})


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_update_device(mock_request, cloud, switch_data):
    response = {"success": True, "message": "Success"}

    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    device = Switch(switch_data["id"], switch_data)

    cloud.update_device_status(device)

    assert mock_request.called


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_update_device_offline(mock_request, cloud, switch_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    device = Switch(switch_data["id"], switch_data)

    with pytest.raises(RentlyAuthError):
        cloud.update_device_status(device)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_update_device_empty(mock_request, cloud):
    with pytest.raises(MissingParametersError):
        cloud.update_device_status(None)
