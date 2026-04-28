class SkyProError(Exception):
    pass


class HttpError(SkyProError):
    pass


class AuthenticationError(HttpError):
    pass
