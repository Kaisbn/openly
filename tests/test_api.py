from openly.api import APIRequestGenerator, APIRouteGenerator
from openly.const import API_DEFAULT_BASE_URL


def test_default_api_path_generator():
    generator = APIRouteGenerator()

    assert generator._BASE_URL == API_DEFAULT_BASE_URL

    assert generator._BASE_LOGIN_URL == API_DEFAULT_BASE_URL


def test_custom_api_path_generator():
    base_url = "http://localhost:8080/"
    generator = APIRouteGenerator(base_url)

    assert generator._BASE_URL == base_url

    assert generator._BASE_LOGIN_URL == base_url


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
