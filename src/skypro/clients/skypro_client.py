import logging
from datetime import date
from types import TracebackType
from typing import Self

from skypro.config import settings

from .dto import AccountDataResponse
from .errors import HttpError
from .http_client import HttpClient

logger = logging.getLogger(__name__)


class SkyProClient:
    base_url = 'https://operation-planning.sky.pro'
    login_url = '/careusers/login/'

    def __init__(self) -> None:
        self._client = HttpClient(base_url=self.base_url, timeout=2)
        self._is_authenticated: bool = False

    async def __aenter__(self) -> Self:
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        return await self._client.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    async def get_account_data(
        self, start_date: date, end_date: date
    ) -> AccountDataResponse:
        await self.login()

        logger.info('Fetching account data from %s to %s', start_date, end_date)
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
        response = await self._client.get('/mentor-cabinet/api/data/', params=params)
        data = await response.json()
        return AccountDataResponse.model_validate(data)

    async def login(self) -> None:
        if self.is_authenticated:
            logger.debug('Skypro api already authenticated')
            return

        logger.info('Authentication skypro api')

        csrf_token = await self._get_csrf_token()
        data = {
            'email': settings.skypro.email,
            'password': settings.skypro.password,
            'csrfmiddlewaretoken': csrf_token,
        }
        response = await self._client.post(self.login_url, data=data)
        if response.url.path == self.login_url:
            raise HttpError('Authentication failed')

        self._is_authenticated = True

    async def _get_csrf_token(self) -> str:
        response = await self._client.options(self.login_url)
        cookie = response.cookies.get('csrftoken')
        if not cookie:
            raise HttpError('CSRF cookie not found')
        return cookie.value
