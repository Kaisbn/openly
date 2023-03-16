import json
import unittest.mock as mock

import pytest

from openly.devices import Hub
from openly.exceptions import InvalidResponseError, RentlyAuthError


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_hubs(mock_request, cloud, hubs_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(hubs_data)
    mock_request.return_value.json.return_value = hubs_data

    result = cloud.get_hubs()

    assert result
    assert isinstance(result, list)
    assert isinstance(result[0], Hub)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_hubs_offline(mock_request, cloud, hubs_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    with pytest.raises(RentlyAuthError):
        cloud.get_hubs()


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_hubs_empty(mock_request, cloud):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = []
    mock_request.return_value.json.return_value = []

    with pytest.raises(InvalidResponseError):
        cloud.get_hubs()


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_hub(mock_request, cloud, hub_data):
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(hub_data)
    mock_request.return_value.json.return_value = hub_data

    result = cloud.get_hub(hub_data["id"])

    assert result
    assert isinstance(result, Hub)

    assert result.id == hub_data["id"]


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_get_hub_offline(mock_request, cloud, hub_data):
    mock_request.return_value.status_code = 401
    cloud.logout()

    with pytest.raises(RentlyAuthError):
        cloud.get_hub(hub_data["id"])


def test_hub_str_id():
    id = "123243-4353ijefef-34212fef-123"
    hub = Hub(id=id)

    assert hub.id == id


def test_hub_int_id():
    id = 123
    hub = Hub(id=id)

    assert hub.id == id


def test_hub_name():
    id = "123243-4353ijefef-34212fef-123"
    hub = Hub(id=id, device_data={"home_name": "Mock Hub"})

    assert hub.name
    assert hub.home_name == hub.name
    assert str(hub) == f"Hub - {hub.id}"


def test_hub_name_none():
    id = "123243-4353ijefef-34212fef-123"
    hub = Hub(id=id)

    with pytest.raises(AttributeError):
        assert not hub.name


def test_hub_cmd():
    id = "123243-4353ijefef-34212fef-123"
    hub = Hub(id=id)

    assert hub.cmd == {}
