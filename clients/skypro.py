import logging

import config

from .errors import SkyProAuthError, SkyProError
from .http_client import HttpClient

logger = logging.getLogger(__name__)


class SkyProClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(
            base_url=config.SKYPRO_BASE_URL, timeout=config.SKYPRO_TIMEOUT_IN_SECONDS
        )
        self._is_authenticated: bool = False

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    async def login(self) -> None:
        if self._is_authenticated:
            logger.debug('Already authenticated in skypro')
            return

        logger.debug('Authenticating in skypro')
        csrf_token = await self._fetch_csrf_token()
        login_data = {
            'email': config.SKYPRO_EMAIL,
            'password': config.SKYPRO_PASSWORD,
            'csrfmiddlewaretoken': csrf_token,
        }
        response = await self.post(
            config.SKYPRO_LOGIN_URL, data=login_data, allow_redirects=False
        )
        if 'sessionid' not in response.cookies:
            logger.error('Authentication failed')
            raise SkyProAuthError('Invalid credentials')

        self._is_authenticated = True
        logger.debug('Authentication to skypro has been completed successfully')

    async def _fetch_csrf_token(self) -> str:
        logger.debug('Fetching csrf token')
        response = await self.options(config.SKYPRO_LOGIN_URL)
        csrf_cookie = response.cookies.get(config.SKYPRO_CSRF_COOKIE_NAME)
        if not csrf_cookie:
            raise SkyProError('CSRF token was not returned by server')
        return csrf_cookie.value
