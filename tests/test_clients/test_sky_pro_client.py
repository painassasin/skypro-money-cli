import asyncio
from collections.abc import AsyncIterator
from urllib.parse import urljoin

import pytest

import config
from clients import SkyProClient
from clients.errors import AuthenticationError, SkyProError
from tests.utils import generate_random_hex


@pytest.fixture
async def skypro_client() -> AsyncIterator[SkyProClient]:
    async with SkyProClient() as c:
        yield c


@pytest.fixture
def login_url() -> str:
    return urljoin(config.SKYPRO_BASE_URL, config.SKYPRO_LOGIN_URL)


@pytest.fixture
def set_csrf_cookie_header() -> dict:
    csrf_cookie_name = config.SKYPRO_CSRF_COOKIE_NAME
    csrf_cookie_value = generate_random_hex(10)
    return {'Set-Cookie': f'{csrf_cookie_name}={csrf_cookie_value}; Path=/; HttpOnly'}


@pytest.fixture
def set_session_id_header() -> dict:
    session_id = generate_random_hex(10)
    return {
        'Set-Cookie': f'sessionid={session_id}; Path=/; HttpOnly',
    }


@pytest.fixture
def valid_fetch_token_response(mock_aioresponse, login_url, set_csrf_cookie_header):
    mock_aioresponse.options(login_url, headers=set_csrf_cookie_header)


@pytest.fixture
def valid_login_response(mock_aioresponse, login_url, set_session_id_header):
    mock_aioresponse.post(login_url, headers=set_session_id_header, status=302)


class TestLogin:
    @pytest.mark.usefixtures('valid_fetch_token_response')
    async def test_invalid_credentials(
        self, skypro_client, mock_aioresponse, login_url
    ):
        """
        Если указаны не правильные данные для подключения,
        то упадет ошибка SkyProAuthError.
        """
        mock_aioresponse.post(login_url, headers={'Location': login_url}, status=302)

        with pytest.raises(AuthenticationError, match='Invalid credentials'):
            await skypro_client.login()
        assert not skypro_client.is_authenticated

    @pytest.mark.usefixtures('valid_fetch_token_response', 'valid_login_response')
    async def test_valid_credentials(self, skypro_client):
        """
        Если указаны верные данные для подключения, то клиент пройдет авторизацию.
        """
        await skypro_client.login()
        assert skypro_client.is_authenticated

    @pytest.mark.usefixtures('valid_fetch_token_response', 'valid_login_response')
    async def test_authenticate_only_once(self, skypro_client, mock_aioresponse):
        """
        Если клиент уже авторизован, то при повторной авторизации ничего не произойдет.
        """
        await asyncio.gather(*(skypro_client.login() for _ in range(3)))
        assert len(mock_aioresponse.requests) == 2

    async def test_csrf_token_not_found(
        self, mock_aioresponse, login_url, skypro_client
    ):
        """Если не удалось получить csrf-токен, упадет ошибка SkyProError."""
        mock_aioresponse.options(login_url, headers={})
        with pytest.raises(SkyProError, match='CSRF token was not returned by server'):
            await skypro_client.login()
