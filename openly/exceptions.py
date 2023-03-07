from urllib.error import HTTPError


class InvalidResponseError(Exception):
    pass


class InvalidParametersError(Exception):
    pass


class MissingParametersError(Exception):
    pass


class RentlyAuthError(Exception):
    pass


class RentlyAPIError(HTTPError):
    pass


class RentlyRateLimitError(RentlyAPIError):
    pass
