import requests


class MockHubResponse:
    @staticmethod
    def json():
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


def test_get_hubs(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockHubResponse()

    monkeypatch.setattr(requests.Session, "get", mock_get)
