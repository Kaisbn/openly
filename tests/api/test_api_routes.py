from openly.api import APIRouteGenerator
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


def test_login_path():
    generator = APIRouteGenerator()

    assert generator.login == API_DEFAULT_BASE_URL + "oauth/token"


def test_custom_path():
    generator = APIRouteGenerator()

    assert generator.devices == API_DEFAULT_BASE_URL + "devices"


def test_custom_path_with_underscores():
    generator = APIRouteGenerator()

    assert generator.device_types == API_DEFAULT_BASE_URL + "device/types"
