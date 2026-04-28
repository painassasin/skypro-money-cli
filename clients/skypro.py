import logging
from types import TracebackType
from typing import Any, Self

from aiohttp import ClientError, ClientResponse, ClientSession, ClientTimeout

import config
from clients.errors import AuthError, SkyProError

logger = logging.getLogger(__name__)


class SkyProClient:
    def __init__(self) -> None:
        self._session: ClientSession | None = None

    async def __aenter__(self) -> Self:
        self._session = ClientSession(
            base_url=config.SKYPRO_BASE_URL,
            timeout=ClientTimeout(total=config.SKYPRO_TIMEOUT_IN_SECONDS),
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if self._session:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            raise RuntimeError(
                f'Session is not initialized. '
                f'Use {self.__class__.__name__}() as client:'
            )
        return self._session

    async def login(self) -> None:
        logger.debug('Authenticating in skypro')

        csrf_token = await self._fetch_csrf_token()
        login_data = {
            'email': config.SKYPRO_EMAIL,
            'password': config.SKYPRO_PASSWORD,
            'csrfmiddlewaretoken': csrf_token,
        }
        response = await self._request(
            'POST', config.SKYPRO_LOGIN_URL, data=login_data, allow_redirects=False
        )
        if 'sessionid' not in response.cookies:
            logger.error('Authentication failed')
            raise AuthError('Invalid credentials')

        logger.debug('Authentication to skypro has been completed successfully')

    async def _fetch_csrf_token(self) -> str:
        logger.debug('Fetching csrf token')
        response = await self._request('OPTIONS', config.SKYPRO_LOGIN_URL)
        csrf_cookie = response.cookies.get(config.SKYPRO_CSRF_COOKIE_NAME)
        if not csrf_cookie:
            raise SkyProError('CSRF token was not returned by server')
        return csrf_cookie.value

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        logger.debug('SkyPro request: %s %s', method, url)

        try:
            response = await self.session.request(method, url, **kwargs)
            response.raise_for_status()
        except ClientError as e:
            logger.exception('SkyPro request failed: %s %s', method, url)
            raise SkyProError(f'Request failed {method} {url}') from e

        return response
