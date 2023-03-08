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
    def __init__(self, url, msg, hdrs, code=500) -> None:
        super().__init__(url=url, code=code, msg=msg, hdrs=hdrs, fp=None)


class RentlyRateLimitError(RentlyAPIError):
    def __init__(self, url, msg, hdrs, code=429) -> None:
        super().__init__(url=url, code=code, msg=msg, hdrs=hdrs)
