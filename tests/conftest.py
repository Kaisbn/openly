import json
import unittest.mock as mock

import pytest

from openly.cloud import RentlyCloud


@pytest.fixture(scope="function")
@mock.patch("openly.cloud.requests.Session.request")
def cloud(mock_request) -> RentlyCloud:
    cloud = RentlyCloud()

    response = {
        "success": True,
        "access_token": "mock_token",
        "id_token": "mock_id_token",
        "refresh_token": "mock_refresh_token",
    }
    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    cloud.login(email="mock_email", password="mock_password")
    return cloud
