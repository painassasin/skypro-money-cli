import json
import random
import re
import string
from asyncio import gather
from collections.abc import AsyncIterator
from datetime import date
from typing import Any
from urllib.parse import urljoin

import pytest

from skypro.clients import SkyProClient
from skypro.clients.errors import HttpError


@pytest.fixture(scope='module')
def login_url() -> str:
    return urljoin(SkyProClient.base_url, SkyProClient.login_url)


@pytest.fixture(scope='module')
def mentor_cabinet_url() -> str:
    return urljoin(SkyProClient.base_url, '/mentor-cabinet/')


@pytest.fixture
def csrf_token() -> str:
    token_length = random.randrange(10, 20)
    return ''.join(random.choice(string.hexdigits) for _ in range(token_length))


@pytest.fixture
async def skypro_client() -> AsyncIterator[SkyProClient]:
    async with SkyProClient() as client:
        yield client


@pytest.fixture(autouse=True)
def mocked_login_url(mock_http, login_url, csrf_token) -> None:
    headers = {'Set-Cookie': f'csrftoken={csrf_token}; Path=/;'}
    mock_http.options(login_url, headers=headers)
    mock_http.get(login_url, headers=headers, content_type='text/html')


@pytest.fixture(autouse=True)
def mocked_mentors_cabinet_url(mock_http, mentor_cabinet_url):
    mock_http.get(mentor_cabinet_url, content_type='text/html', status=200)


@pytest.fixture(scope='module')
def account_data_response(fixtures_dir) -> dict[str, Any]:
    fixture_path = fixtures_dir / 'account_data_response.json'
    return json.loads(fixture_path.read_text())


@pytest.fixture
def mocked_login(mocker):
    return mocker.patch.object(SkyProClient, 'login', new=mocker.AsyncMock())


async def test_success_login(mock_http, skypro_client, login_url):
    mock_http.post(login_url, headers={'Location': '/mentor-cabinet/'}, status=302)
    await skypro_client.login()
    assert skypro_client.is_authenticated is True


async def test_do_not_login_twice(skypro_client, mock_http, login_url):
    mock_http.post(login_url, headers={'Location': '/mentor-cabinet/'}, status=302)
    tasks = (skypro_client.login() for _ in range(10))

    await gather(*tasks)

    assert len(mock_http.requests) == 2
    mock_http.assert_any_call(login_url, 'POST')
    mock_http.assert_any_call(login_url, 'OPTIONS')


async def test_invalid_credentials(skypro_client, mock_http, login_url):
    mock_http.post(login_url, headers={'Location': login_url}, status=302)

    with pytest.raises(HttpError, match='Authentication failed'):
        await skypro_client.login()

    assert skypro_client.is_authenticated is False


async def test_get_account_data_success(
    skypro_client, mock_http, account_data_response, mocked_login
):
    api_url = urljoin(SkyProClient.base_url, '/mentor-cabinet/api/data/')
    mock_http.get(re.compile(rf'^{api_url}'), payload=account_data_response, status=200)
    start_date, end_date = date(2021, 1, 1), date(2021, 1, 2)

    data = await skypro_client.get_account_data(start_date, end_date)

    assert data.services_summary.homework == 36
    assert data.services_summary.coursework == 8
    assert data.services_summary.diploma == 12
    assert data.services_summary.live == 6
    assert data.services_summary.individual_consultation == 3
    mocked_login.assert_awaited_once()
