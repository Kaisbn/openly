import json
import unittest.mock as mock

import pytest

from openly.cloud import RentlyCloud


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def hubs_data() -> dict:
    return {
        "total_records": 1,
        "page": 1,
        "per_page": 1000,
        "hubs": [
            {
                "id": "123243-4353ijefef-34212fef-123",
                "allowed_hub_codes": 12,
                "time_zone": "Mock time",
                "home_name": "Mock Home",
                "occupant_setting": "123",
                "address": "123 St, Mock city, MC 12345",
                "state": "MC",
                "city": "Mock city",
                "zipcode": "12345",
                "longitude": "-10.0432432",
                "latitude": "12.34567",
                "primary_resident_occupied": True,
                "camera": False,
                "master_code": "123456",
                "serial_no": 12345,
                "property_url": "mock/property",
                "unit_code": "",
                "api_code": "",
                "vacation_code_occupied": False,
                "street_address": "123 St",
                "lock_code_count": 2,
                "topic_name": "mock/topic",
                "is_active": True,
                "active_from": "1/1/2000 12:00 am",
                "active_to": "12/31/2030 11:59 pm",
                "user_type": "admin",
                "status": "Online",
            }
        ],
    }


@pytest.fixture(scope="module")
def hub_data() -> dict:
    return {
        "id": "123243-4353ijefef-34212fef-123",
        "allowed_hub_codes": 12,
        "time_zone": "Mock time",
        "home_name": "Mock Home",
        "occupant_setting": "123",
        "address": "123 St, Mock city, MC 12345",
        "state": "MC",
        "city": "Mock city",
        "zipcode": "12345",
        "longitude": "-10.0432432",
        "latitude": "12.34567",
        "primary_resident_occupied": True,
        "camera": False,
        "master_code": "123456",
        "serial_no": 12345,
        "property_url": "mock/property",
        "unit_code": "",
        "api_code": "",
        "vacation_code_occupied": False,
        "street_address": "123 St",
        "lock_code_count": 2,
        "topic_name": "mock/topic",
        "settings": {"time_zone": "Mock time", "monitoring": "disarm"},
        "status": {
            "csq": "12,39",
            "imei": "Mock IMEI",
            "imsi": "MOCK IMSI",
            "mode": "central",
            "fwVer": "0.0.0",
            "model": "Mock model",
            "battery": 66,
            "message": "Failed to scan the slave node.",
            "nodeList": [
                1,
                0,
                0,
            ],
            "heartBeat": "2021-01-01T08:20:49.224Z",
            "lockFWVer": ["xxxxx", "zzzzz"],
            "serialSsh": True,
            "HWSerialNo": "Mock HW Serial No",
            "add_device": {
                "7": ["dimmable_switch", "xxx"],
                "8": ["lock", "xxx"],
            },
            "board_type": "V3",
            "network_type": "cellular",
            "signal_query": {
                "csq": 10,
                "wifi_ss": "-1",
                "curr_conn_type": "cellular",
            },
            "remove_device": {"2": "delete"},
            "lastRefreshDate": "2021-11-09T09:00:16.230Z",
            "readyForBleCmds": True,
            "signal_strength": "18",
            "scanDeviceReport": ["xxx", -100, 1, 1, 100],
            "powerNotification": ["0xc1", 87],
            "lastRemoveFailedNode": "2022-11-17T10:39:57.119Z",
            "updateHubFWverErrReport": "Cookie is not valid",
        },
        "show_monitoring_feature": True,
        "assigned_date": "2012-07-23",
    }


@pytest.fixture(scope="module")
def lock_data() -> dict:
    return {
        "id": "12344-4543545-3546",
        "device_name": "Mock Lock",
        "occupant_setting": "Mock Lock",
        "device_type": "lock",
        "iot_thing_name": "mock id",
        "remote_device_id": "8",
        "zwave_security": "non_secure",
        "model_number": "123-345",
        "shared_area": False,
        "location": None,
        "power_source": "battery",
        "two_way_power_source": False,
        "topic_name": "$mock/topic",
        "last_activity": 160000000,
        "manufacturer": "Mock manufacturer",
        "product_name": "Mock lock",
        "settings": {},
        "status": {
            "mode": {"type": "locked"},
            "codes": {"1": None, "2": "123456"},
            "battery": 100,
            "max_slots": 250,
            "power_source": "battery",
            "zwave_signal": 3,
            "setting_errors": {"lock_codes": {"xxx": None}},
            "battery_zwave": 96,
        },
        "auto_lock_config": {
            "is_auto_lock_supported": True,
            "auto_lock_enabled": True,
            "auto_lock_timer": "60",
            "supported_timers": [30, 60, 120, 180],
            "reported": {"auto_lock_enabled": True, "auto_lock_timer": "60"},
        },
        "log_mindate": "2021-10-20T00:00:00-08:00",
    }


@pytest.fixture(scope="module")
def switch_data() -> dict:
    return {
        "id": "1232434-abc343434",
        "device_name": "Mock Switch",
        "occupant_setting": "Mock Switch",
        "device_type": "dimmable_switch",
        "iot_thing_name": "mock id",
        "remote_device_id": "2",
        "zwave_security": "non_secure",
        "model_number": "123-345",
        "shared_area": False,
        "location": None,
        "power_source": "main",
        "two_way_power_source": None,
        "topic_name": "$mock/topic",
        "last_activity": 160000000,
        "manufacturer": "Mock manufacturer",
        "product_name": "Mock switch",
        "settings": {"hold_duration": 240},
        "status": {
            "mode": "off",
            "power": 0,
            "source": "physical",
            "hold_until": "2021-05-27T17:28:27.819Z",
            "power_source": "main",
            "zwave_signal": 3,
        },
        "log_mindate": "2022-11-25T00:00:00-08:00",
    }
