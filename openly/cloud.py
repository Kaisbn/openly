import json
from datetime import datetime
from time import sleep
from typing import Any, Optional, Union

import jwt
import requests

import openly.util as util
from openly.api import APIRequestGenerator
from openly.const import (
    API_RETRY_ATTEMPTS,
    API_RETRY_TIME,
    DEVICES,
    HEADER_KEY_AUTHORIZATION,
    HEADER_KEY_CONTENT_TYPE,
    HEADER_KEY_USER_AGENT,
    HEADER_VALUE_CONTENT_TYPE,
    HEADER_VALUE_USER_AGENT,
)
from openly.devices import Hub
from openly.devices.base_device import BaseDevice
from openly.exceptions import (
    InvalidResponseError,
    MissingParametersError,
    RentlyAPIError,
    RentlyAuthError,
)

_LOGGER = util.setupLogger()


class RentlyCloud:
    _api: APIRequestGenerator
    _auth: dict = {}
    _session: requests.Session
    _token: dict = {}  # decoded token

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
        self._session = requests.Session()
        self._api = APIRequestGenerator(url, login_url)

    @property
    def headers(self) -> dict:
        """HTTP Headers to use"""
        headers = {
            HEADER_KEY_USER_AGENT: HEADER_VALUE_USER_AGENT,
            HEADER_KEY_CONTENT_TYPE: HEADER_VALUE_CONTENT_TYPE,
        }

        if self.token:
            headers[HEADER_KEY_AUTHORIZATION] = self.token

        return headers

    @property
    def token(self) -> Union[str, None]:
        """Access token"""
        if not self._auth or "access_token" not in self._auth:
            return None
        return self._auth["access_token"]

    @token.setter
    def token(self, value: str) -> None:
        """Set token"""
        try:
            self._token = jwt.decode(
                value, options={"verify_signature": False}
            )
            self._auth["access_token"] = value
        except jwt.ExpiredSignatureError:
            self.logout()

    @token.deleter
    def token(self) -> None:
        """Delete token"""
        del self._auth
        del self._token

    @property
    def connected(self) -> bool:
        """Connection status"""
        if not self._token:
            return False

        return self._token["exp"] > datetime.now().timestamp()

    def call(self, req: dict[str, Any]) -> dict[str, Any]:
        """
        Method to make an HTTP request to the API using the provided request
        parameters

        Args:
            req (dict[str, Any]): Request parameters

        Raises:
            RentlyAPIError: More details provided in the exception message

        Returns:
            dict[str, Any]: JSON Response from the server
        """
        attempts = 0
        while attempts < API_RETRY_ATTEMPTS:
            attempts += 1

            try:
                res = self._session.request(
                    method=req["method"],
                    url=req["url"],
                    data=req.get("body"),
                    headers=self.headers,
                )

                _LOGGER.debug(
                    "Received API response: %s, %s",
                    res.status_code,
                    res.content,
                )

                res.raise_for_status()
                break
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 429:
                    _LOGGER.debug(
                        (
                            "Rently sent a 429 Too Many Requests (attempt:"
                            " %d/%d), sleeping for %d seconds and trying"
                            " again"
                        ),
                        attempts,
                        API_RETRY_ATTEMPTS,
                        API_RETRY_TIME,
                    )

                    sleep(API_RETRY_TIME)
                    continue
                else:
                    _LOGGER.error(
                        "Request to %s failed: %s",
                        req["url"],
                        err.response.content,
                    )
                    raise RentlyAPIError(
                        url=req["url"],
                        code=err.response.status_code,
                        hdrs=err.response.headers,
                        msg=err.response.content,
                    ) from err

        if attempts == API_RETRY_ATTEMPTS:
            raise RentlyAPIError(
                url=req["url"],
                code=429,
                hdrs=None,
                msg="Too many requests",
            )

        return res.json()

    def login(self, email: str, password: str) -> bool:
        """
        Login to an account using credentials and retrieve token

        Args:
            email (str)
            password (str)

        Raises:
            MissingParametersError: Credentials not provided
            RentlyAuthError: Unauthorized

        Returns:
            bool: Connection status
        """
        if not email or not password:
            raise MissingParametersError(
                "Email and password must be provided to authenticate."
            )

        res = self.call(self._api.get_oauth_token_request(email, password))

        if not res.get("success") or "access_token" not in res:
            raise RentlyAuthError(res.get("message", "Login failed"))

        # Save auth response
        self._auth = res
        # Set token and verify
        self.token = res["access_token"]
        if not self.token:
            return False

        # Update session headers
        self._session.headers.update(self.headers)

        return True

    def refresh(self) -> bool:
        """
        Refresh the existing token and retrieve a new one

        Returns:
            bool: Connection status
        """
        if not self._auth:
            return MissingParametersError("No token to refresh")

        res = self.call(self._api.get_oauth_refresh_request(self._auth["refresh_token"]))

        if not res.get("success") or "access_token" not in res:
            raise RentlyAuthError(res.get("message", "Refresh failed"))

        # Save auth response
        self.token = res["access_token"]
        if not self.token:
            return False

        # Update session headers
        self._session.headers.update(self.headers)

    def logout(self) -> None:
        """
        Logout user

        Returns:
            None
        """
        # Remove auth payload
        del self.token
        # Remove auth header
        self._session.headers.update(self.headers)

    def get_hubs(self) -> list[Hub]:
        """
        Retrieve list of hubs

        Raises:
            RentlyAuthError: Unauthenticated

        Returns:
            list[Hub]: List of Hub objects
        """
        if not self.connected:
            raise RentlyAuthError("Unauthenticated")

        hubs_data = self.call(self._api.get_hub_list_request())
        if "hubs" not in hubs_data:
            raise InvalidResponseError("Invalid hubs list")

        _LOGGER.debug("Retrieving list of hubs")

        return [Hub(id=h["id"]) for h in hubs_data["hubs"]]

    def get_hub(self, hub_id: Union[str, int]) -> Hub:
        """
        Retrieve single hub

        Args:
            hub_id (Union[str, int]): ID of the hub to retrieve

        Raises:
            RentlyAuthError: Unauthenticated

        Returns:
            Hub: Retrieved object
        """
        if not self.connected:
            raise RentlyAuthError("Unauthenticated")

        _LOGGER.debug("Retrieving hub with ID %s", hub_id)

        return Hub(
            id=hub_id,
            device_data=self.call(self._api.get_hub_detail_request(hub_id)),
        )

    def get_devices(self, hub_id: Union[str, int]) -> list[BaseDevice]:
        """
        Retrieve list of devices

        Args:
            hub_id (Union[str, int]): ID of the hub to retrieve devices from

        Raises:
            RentlyAuthError: Unauthenticated

        Returns:
            list[BaseDevice]: List of device objects (inherit BaseDevice)
        """
        if not self.connected:
            raise RentlyAuthError("Unauthenticated")

        devices_data = self.call(self._api.get_device_list_request(hub_id))
        if not devices_data:
            raise InvalidResponseError("Invalid devices list")

        _LOGGER.debug("Retrieving list of devices for hub with ID %s", hub_id)
        device_objs = []

        for device_type, device_list in devices_data.items():
            if device_type in DEVICES:
                for device_data in device_list:
                    device_objs.append(
                        DEVICES[device_type](
                            id=device_data["id"],
                            device_data=device_data,
                        )
                    )

        return device_objs

    def get_device(self, device_id: Union[str, int]) -> BaseDevice:
        """
        Retrieve single device

        Args:
            device_id (Union[str, int]): ID of the device to retrieve

        Raises:
            RentlyAuthError: Unauthenticated

        Returns:
            BaseDevice: Retrieved object
        """
        if not self.connected:
            raise RentlyAuthError("Unauthenticated")

        device_data = self.call(self._api.get_device_detail_request(device_id))
        if not device_data:
            raise InvalidResponseError(f"Unable to fetch device {device_id}")

        device_type = device_data.get("device_type")
        if not device_type or device_type not in DEVICES:
            raise InvalidResponseError(f"Invalid device: {device_data}")

        _LOGGER.debug("Retrieving device with ID %s", device_id)

        return DEVICES[device_type](id=device_id, device_data=device_data)

    def send_command(self, device_id: Union[str, int], command: Any) -> None:
        """
        Send a command to a device

        Args:
            device_id (Union[str, int]): ID of the device to command
            command (Any): Action to execute

        Raises:
            RentlyAuthError: Unauthenticated
        """
        if not self.connected:
            raise RentlyAuthError("Unauthenticated")

        _LOGGER.debug(
            "Sending payload %s to %s", json.dumps(command), device_id
        )

        self.call(self._api.update_device_request(device_id, command))

    def update_device_status(self, device) -> None:
        """
        Send the current command to the specified device

        Args:
            device (BaseDevice): Device to update

        Raises:
            RentlyAuthError: Unauthenticated
            MissingParametersError: Parameters supplied are not valid
        """
        if not device or not isinstance(device, BaseDevice):
            raise MissingParametersError("Device not found")

        _LOGGER.debug(
            "Sending payload %s to %s",
            json.dumps(device.cmd),
            device.id,
        )

        self.send_command(device.id, device.cmd)
