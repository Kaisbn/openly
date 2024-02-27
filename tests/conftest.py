import json
import unittest.mock as mock

import pytest

from openly.cloud import RentlyCloud


@pytest.fixture(scope="module")
def tokens():
    """Fixture to return the tokens for the user login"""
    return {
        "access_token": (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
            ".eyJpc3MiOiJSZW50bHkiLCJpYXQiOjE2Nzc0NDM5MDUsImV4cCI6Mj"
            "A1NjA0ODcwNSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoid"
            "GVzdEBleGFtcGxlLmNvbSJ9.NP6hspRMioyAspvKW1RpkEiDU1tseWN"
            "P_dv8ef5FhPY"
        ),
        "id_token": (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ"
            "pc3MiOiJSZW50bHkiLCJpYXQiOjE2Nzc0NDM5MDUsImV4cCI6MjA1Nj"
            "A0ODcwNSwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoidGVzd"
            "EBleGFtcGxlLmNvbSJ9.cvQhbOv1mGqT-gWMI9Xp8V3x-BhWLLeuRxp"
            "162Xf4rM"
        ),
        "refresh_token": "mock_refresh_token",
    }


@pytest.fixture(scope="function")
@mock.patch("openly.cloud.requests.Session.request")
def cloud(mock_request, tokens) -> RentlyCloud:
    """Fixture to login the user and return the instance"""
    cloud_obj = RentlyCloud()
    response = tokens | {"success": True}

    mock_request.return_value.status_code = 200
    mock_request.return_value.content = json.dumps(response)
    mock_request.return_value.json.return_value = response

    cloud_obj.login(email="mock_email", password="mock_password")
    return cloud_obj
