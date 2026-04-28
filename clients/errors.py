class SkyProError(Exception):
    pass


class HttpError(SkyProError):
    pass


class SkyProAuthError(SkyProError):
    pass
