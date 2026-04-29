from collections.abc import AsyncIterator
from http import HTTPStatus

import pytest

from clients.errors import HttpError
from clients.http_client import HttpClient


@pytest.fixture
def base_url() -> str:
    return 'http://example.com'


@pytest.fixture
async def http_client(base_url) -> AsyncIterator[HttpClient]:
    async with HttpClient(base_url, timeout=1) as client:
        yield client


async def test_success_response(http_client, mock_http):
    mock_http.get('http://example.com/test/', status=200)
    response = await http_client.get('test/')
    assert response.status == HTTPStatus.OK


async def test_bad_request(http_client, mock_http):
    payload = {'status': 'error', 'code': 'validation_error'}
    mock_http.get('http://example.com/test/', payload=payload, status=400)

    with pytest.raises(HttpError, match='HTTP 400: GET test/'):
        await http_client.get('test/')


async def test_timeout_error(http_client, mock_http):
    mock_http.get('http://example.com/test/', timeout=True)
    with pytest.raises(HttpError, match='Network error: GET test/'):
        await http_client.get('test/')
