import pytest


@pytest.fixture(scope="function")
def devices_data() -> dict:
    return {
        "thermostat": [
            {
                "id": "123243-4353ijefef-34212fef-123",
                "device_name": "Mock Thermostat",
                "occupant_setting": "Mock Thermostat",
                "device_type": "thermostat",
                "iot_thing_name": "mock id",
                "topic_name": "$mock/topic",
            }
        ],
        "lock": [
            {
                "id": "12345-243243rwre-23423-23423",
                "device_name": "Mock Lock",
                "occupant_setting": "Mock Lock",
                "device_type": "lock",
                "iot_thing_name": "mock id",
                "topic_name": "$mock/topic",
            }
        ],
    }


@pytest.fixture(scope="function")
def switch_data() -> dict:
    return {
        "id": "1232434-abc343434",
        "device_name": "Mock Switch",
        "occupant_setting": "Mock Switch",
        "device_type": "switch",
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
        "status": {
            "mode": "off",
            "source": "physical",
            "hold_until": "2021-05-27T17:28:27.819Z",
            "power_source": "main",
            "zwave_signal": 3,
        },
        "log_mindate": "2022-11-25T00:00:00-08:00",
    }
