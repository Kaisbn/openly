import json
import unittest.mock as mock

import pytest
import requests

from openly.cloud import RentlyCloud
from openly.const import (
    HEADER_KEY_AUTHORIZATION,
    HEADER_KEY_CONTENT_TYPE,
    HEADER_KEY_USER_AGENT,
    HEADER_VALUE_CONTENT_TYPE,
    HEADER_VALUE_USER_AGENT,
)
from openly.exceptions import (
    MissingParametersError,
    RentlyAPIError,
    RentlyAuthError,
)


@pytest.fixture(scope="function")
def cloud():
    return RentlyCloud()


def test_headers(cloud):
    assert HEADER_KEY_USER_AGENT in cloud.headers
    assert HEADER_KEY_CONTENT_TYPE in cloud.headers
    assert cloud.headers[HEADER_KEY_USER_AGENT] == HEADER_VALUE_USER_AGENT
    assert cloud.headers[HEADER_KEY_CONTENT_TYPE] == HEADER_VALUE_CONTENT_TYPE


@mock.patch("openly.cloud.requests.Session.request")
def test_login_success(mock_request, cloud, tokens):
    response = tokens | {"success": True}
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    result = cloud.login(email="mock_email", password="mock_password")

    assert result is True
    assert cloud.connected is True

    assert cloud._auth == response
    assert cloud.token == response["access_token"]

    assert HEADER_KEY_AUTHORIZATION in cloud.headers
    assert cloud.headers[HEADER_KEY_AUTHORIZATION] == cloud.token


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_login_bad_credentials(mock_request, cloud):
    response = {"success": False, "message": "Incorrect username or password."}
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    with pytest.raises(RentlyAuthError):
        cloud.login("mock_email", "mock_password")

    assert not cloud.connected
    assert not cloud.token

    assert HEADER_KEY_AUTHORIZATION not in cloud.headers


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_login_missing_credentials(mock_request, cloud):
    response = {"success": False, "message": "Invalid request body"}
    mock_request.return_value.status_code = 400
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    with pytest.raises(MissingParametersError):
        cloud.login("mock_email", None)


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
@mock.patch("openly.cloud.sleep", return_value=None)
def test_login_rate_limit(patched_sleep, mock_request, cloud):
    mock_response = requests.models.Response()
    mock_response.status_code = 429
    mock_request.return_value = mock_response

    with pytest.raises(RentlyAPIError) as err:
        cloud.login("mock_email", "mock_password")
        assert err.value.status_code == 429


@mock.patch("openly.cloud.requests.Session.request", autospec=True)
def test_login_server_error(mock_request, cloud):
    mock_response = requests.models.Response()
    mock_response.status_code = 500
    mock_request.return_value = mock_response

    with pytest.raises(RentlyAPIError):
        cloud.login("mock_email", "mock_password")

    assert not cloud.connected
    assert not cloud.token

    assert HEADER_KEY_AUTHORIZATION not in cloud.headers
