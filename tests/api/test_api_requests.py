from openly.api import APIRequestGenerator
from openly.const import API_DEFAULT_BASE_URL


def test_default_api_request_generator():
    generator = APIRequestGenerator()

    assert generator.api_routes
    assert generator.api_routes._BASE_URL == API_DEFAULT_BASE_URL
    assert generator.api_routes._BASE_LOGIN_URL == API_DEFAULT_BASE_URL


def test_custom_api_generator_generator():
    base_url = "http://localhost:8080/"
    generator = APIRequestGenerator(base_url)

    assert generator.api_routes
    assert generator.api_routes._BASE_URL == base_url
    assert generator.api_routes._BASE_LOGIN_URL == base_url


def test_oauth_request():
    generator = APIRequestGenerator()
    request = generator._get_oauth_token_request(
        email="test@test.com", password="test"
    )

    assert request["method"] == "POST"
    assert request["url"] == API_DEFAULT_BASE_URL + "oauth/token"


def test_hub_list_request():
    generator = APIRequestGenerator()
    request = generator._get_hub_list_request()

    assert request["method"] == "GET"
    assert request["url"] == API_DEFAULT_BASE_URL + "hubs"


def test_hub_detail_request():
    generator = APIRequestGenerator()
    request = generator._get_hub_detail_request(hub_id=1)

    assert request["method"] == "GET"
    assert request["url"] == API_DEFAULT_BASE_URL + "hubs/1"
