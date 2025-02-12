import json
from typing import Any, Optional, Union

import openly.const as const


class APIRouteGenerator:
    """
    URL path generator class
    """

    _BASE_URL: str = const.API_DEFAULT_BASE_URL

    def __init__(
        self, url: Optional[str] = None, login_url: Optional[str] = None
    ) -> None:
        """
        Constructor

        Args:
            url (str): Base URL to reach Rently's API.
                Defaults to the URL provided in the documentation
            login_url (str): Base URL to reach Rently's login API,
                useful when login is separated from the main API.
                Defaults to the Base URL above.
        """
        if url:
            self._BASE_URL = url

    def __getattr__(self, attr: str) -> str:
        """
        Override __getattr__ magic method to return generated URL paths

        Args:
            attr (str): Endpoint to retreive

        Returns:
            str: URL Path
        """
        return self._BASE_URL + attr.lower().replace("_", "/")


class APIRequestGenerator:
    """
    API Request generator class
    """

    api_routes: APIRouteGenerator
    login_api_routes: APIRouteGenerator

    def __init__(
        self, url: Optional[str] = None, login_url: Optional[str] = None
    ) -> None:
        """
        Constructor

        Args:
            url (str): Base URL to reach Rently's API.
                Defaults to the URL provided in the documentation
            login_url (str): Base URL to reach Rently's login API,
                useful when login is separated from the main API.
                Defaults to the Base URL above.
        """
        self.api_routes = APIRouteGenerator(url)
        self.login_api_routes = APIRouteGenerator(login_url)

    def get_oauth_token_request(self, email: str, password: str) -> dict[str, Any]:
        """
        Retrieve authentication token using credentials

        Args:
            email (str)
            password (str)

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "POST",
            "url": self.login_api_routes.OAUTH_TOKEN,
            "body": json.dumps({"email": email, "password": password}),
        }

    def get_oauth_refresh_request(self, refresh_token: str) -> dict[str, Any]:
        """
        Retrieve a new authentication token using a refresh token

        Args:
            refresh_token (str)

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "POST",
            "url": self.login_api_routes.API_REFRESHTOKEN,
            "body": json.dumps({"refreshtoken": refresh_token}),
        }

    def get_hub_list_request(self) -> dict[str, Any]:
        """
        Retrieve list of hubs

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "GET",
            "url": self.api_routes.hubs,
        }

    def get_hub_detail_request(self, hub_id: Union[str, int]) -> dict[str, Any]:
        """
        Retrieve single hub information

        Args:
            hub_id (Union[str, int]): ID of the hub to retrieve

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "GET",
            "url": getattr(self.api_routes, f"hubs_{hub_id}"),
        }

    def get_device_list_request(self, hub_id: Union[str, int]) -> dict[str, Any]:
        """
        Retrieve list of devices for a single hub

        Args:
            hub_id (Union[str, int]): ID of the hub to retrieve devices from

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "GET",
            "url": getattr(self.api_routes, f"hubs_{hub_id}_devices"),
        }

    def get_device_detail_request(self, device_id: Union[str, int]) -> dict[str, Any]:
        """
        Retrieve list of devices for a single hub

        Args:
            device_id (Union[str, int]): ID of the device to retrieve

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "GET",
            "url": getattr(self.api_routes, f"devices_{device_id}"),
        }

    def update_device_request(
        self, device_id: Union[str, int], commands: Any
    ) -> dict[str, Any]:
        """
        Push one or multiple commands to a specific device

        Args:
            device_id (Union[str, int]): ID of the device to retrieve
            commands (Any): Command(s) to send to the device

        Returns:
            dict[str, Any]: Request parameters
        """
        return {
            "method": "PUT",
            "url": getattr(self.api_routes, f"devices_{device_id}"),
            "body": json.dumps({"commands": commands}),
        }
