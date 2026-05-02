import re
from asyncio import gather
from datetime import date
from http import HTTPStatus

import pytest

from skypro.api.http.client import HttpClient
from skypro.api.skypro.client import SkyProClient
from skypro.api.skypro.dto import AccountDataResponse
from skypro.api.skypro.errors import AuthenticationError
from skypro.config.settings import settings


@pytest.fixture(autouse=True)
def skypro_credentials(mocker):
    mocker.patch.object(settings.skypro, 'email', 'mentor@example.com')
    mocker.patch.object(settings.skypro, 'password', 'secret-password')


@pytest.fixture
async def http_client():
    async with HttpClient() as client:
        yield client


@pytest.fixture
def skypro_client(http_client):
    return SkyProClient(http_client)


@pytest.fixture
def login_url_response(httpx_mock):
    httpx_mock.add_response(
        url='https://operation-planning.sky.pro/careusers/login/',
        headers={'set-cookie': 'csrftoken=test-csrf-token; Path=/'},
    )


@pytest.fixture
def mocked_login(mocker):
    return mocker.patch.object(SkyProClient, 'login')


@pytest.fixture
def account_data_response() -> dict:
    return {
        'services_summary': {
            'ДЗ': 1,
            'КР': 2,
            'ДР': 3,
            'Лайв': 4,
            'ИК': 5,
        }
    }


@pytest.mark.usefixtures('login_url_response')
async def test_success_login_set_is_authenticated_status(skypro_client, httpx_mock):
    _build_login_redirect_response(httpx_mock, '/mentor-cabinet/')
    await skypro_client.login()
    assert skypro_client.is_authenticated


@pytest.mark.usefixtures('login_url_response')
async def test_invalid_credentials_login_failed(skypro_client, httpx_mock):
    _build_login_redirect_response(httpx_mock, '/careusers/login/')

    with pytest.raises(AuthenticationError, match='Authentication failed'):
        await skypro_client.login()

    assert not skypro_client.is_authenticated


@pytest.mark.usefixtures('login_url_response')
async def test_silence_skip_if_login_twice(skypro_client, httpx_mock):
    _build_login_redirect_response(httpx_mock, '/mentor-cabinet/')
    tasks = (skypro_client.login() for _ in range(10))

    await gather(*tasks)

    assert len(httpx_mock.get_requests()) == 3


async def test_get_account_data(
    skypro_client, httpx_mock, mocked_login, account_data_response
):
    httpx_mock.add_response(
        method='GET',
        url=re.compile(r'https://operation-planning.sky.pro/mentor-cabinet/api/data/.*'),
        json=account_data_response,
    )
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)

    data = await skypro_client.get_account_data(start_date, end_date)

    assert data == AccountDataResponse(**account_data_response)
    mocked_login.assert_called_once()


def _build_login_redirect_response(httpx_mock, redirect_url):
    httpx_mock.add_response(
        method='POST', headers={'Location': redirect_url}, status_code=HTTPStatus.FOUND
    )
    httpx_mock.add_response(method='GET')
