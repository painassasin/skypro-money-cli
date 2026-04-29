import logging
from datetime import date

from config import settings
from .dto import AccountData
from .errors import AuthenticationError, SkyProError
from .http_client import AuthAuthMixin, HttpClient, login_required

logger = logging.getLogger(__name__)


class SkyProClient(AuthAuthMixin, HttpClient):
    def __init__(self) -> None:
        super().__init__(
            base_url=settings.skypro.base_url,
            timeout=settings.skypro.timeout_in_seconds
        )

    @login_required
    async def get_account_data(self, start_date: date, end_date: date) -> AccountData:
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        }
        response = await self.get('/mentor-cabinet/api/data/', params=params)
        data = await response.json()
        return AccountData.model_validate(data)

    async def login(self) -> None:
        if self.is_authenticated:
            logger.debug('Already authenticated in skypro')
            return

        logger.debug('Authenticating in skypro')
        csrf_token = await self._fetch_csrf_token()
        login_data = {
            'email': settings.skypro.email,
            'password': settings.skypro.password,
            'csrfmiddlewaretoken': csrf_token,
        }
        response = await self.post(
            settings.skypro.login_url, data=login_data, allow_redirects=False
        )
        if 'sessionid' not in response.cookies:
            logger.error('Authentication failed')
            raise AuthenticationError('Invalid credentials')

        self._authenticate()

    async def _fetch_csrf_token(self) -> str:
        logger.debug('Fetching csrf token')
        response = await self.options(settings.skypro.login_url)
        csrf_cookie = response.cookies.get(settings.skypro.csrf_cookie_name)
        if not csrf_cookie:
            raise SkyProError('CSRF token was not returned by server')
        return csrf_cookie.value
