from http import HTTPStatus

import httpx
import pytest
from pytest_httpx import HTTPXMock

from skypro.infra.http.client import HttpClient
from skypro.infra.http.errors import HttpError


@pytest.fixture
def url() -> str:
    return 'http://example.com'


async def test_timeout_error(httpx_mock: HTTPXMock, url: str, http_client: HttpClient):
    httpx_mock.add_exception(httpx.TimeoutException('Request timed out'))
    with pytest.raises(HttpError, match='Network error'):
        await http_client.request('GET', url)


async def test_invalid_response_error(
    httpx_mock: HTTPXMock, http_client: HttpClient, url: str
):
    httpx_mock.add_response(url=url, status_code=HTTPStatus.BAD_REQUEST)
    with pytest.raises(HttpError, match=f'HTTP 400: GET {url}'):
        await http_client.request('GET', url)
