import logging
from datetime import date

from skypro.config import get_settings
from skypro.infra.api.base import BaseApiClient
from skypro.infra.api.errors import AuthenticationError
from skypro.infra.http.client import HttpClient

from .dto import AccountDataResponse

logger = logging.getLogger(__name__)


class SkyProClient(BaseApiClient):
    base_url = 'https://operation-planning.sky.pro'
    login_url = '/careusers/login/'

    def __init__(self, http_client: HttpClient) -> None:
        super().__init__(http_client)
        self._is_authenticated = False

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    async def get_account_data(
        self, start_date: date, end_date: date
    ) -> AccountDataResponse:
        await self.login()

        logger.info('Fetching account data from %s to %s', start_date, end_date)

        response = await self._get(
            '/mentor-cabinet/api/data/',
            params={
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
            },
        )

        return AccountDataResponse.model_validate(response.json())

    async def login(self) -> None:
        if self._is_authenticated:
            logger.debug('SkyPro already authenticated')
            return

        logger.info('Authenticating in SkyPro')

        csrf_token = await self._get_csrf_token()

        response = await self._post(
            self.login_url,
            data={
                'email': get_settings().skypro.email,
                'password': get_settings().skypro.password_value,
                'csrfmiddlewaretoken': csrf_token,
            },
        )

        if response.url.path == self.login_url:
            raise AuthenticationError('Authentication failed')

        self._is_authenticated = True

        logger.info('SkyPro authentication successful')

    async def _get_csrf_token(self) -> str:
        logger.debug('Fetching csrf token')

        await self._get(self.login_url)

        csrf_token = self.cookies.get('csrftoken')
        if csrf_token is None:
            raise AuthenticationError('CSRF token not found')

        return csrf_token
