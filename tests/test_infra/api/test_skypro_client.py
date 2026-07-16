import re
from asyncio import gather
from datetime import date
from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from pytest_httpx import HTTPXMock
from pytest_mock import MockFixture

from skypro.infra.api.errors import AuthenticationError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.api.skypro.dto import AccountDataResponse


@pytest.fixture
def login_url_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url='https://operation-planning.sky.pro/careusers/login/',
        headers={'set-cookie': 'csrftoken=test-csrf-token; Path=/'},
    )


@pytest.fixture
def mocked_login(mocker: MockFixture) -> MagicMock:
    return mocker.patch.object(SkyProClient, 'login')


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


async def test_get_account_data(skypro_client, httpx_mock, mocked_login, account_data):
    httpx_mock.add_response(
        method='GET',
        url=re.compile(
            r'https://operation-planning.sky.pro/mentor-cabinet/api/data/.*'
        ),
        json=account_data,
    )
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)

    data = await skypro_client.get_account_data(start_date, end_date)

    assert data == AccountDataResponse(**account_data)
    mocked_login.assert_called_once()


async def test_failed_to_fetch_csrf_token_error(
    skypro_client: SkyProClient, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url='https://operation-planning.sky.pro/careusers/login/',
    )

    with pytest.raises(AuthenticationError, match='CSRF token not found'):
        await skypro_client.login()


def _build_login_redirect_response(httpx_mock: HTTPXMock, redirect_url: str) -> None:
    httpx_mock.add_response(
        method='POST', headers={'Location': redirect_url}, status_code=HTTPStatus.FOUND
    )
    httpx_mock.add_response(method='GET')
