from collections.abc import AsyncIterator

import pytest

from clients.errors import HttpError
from clients.http_client import HttpClient


@pytest.fixture
async def http_client() -> AsyncIterator[HttpClient]:
    async with HttpClient(base_url='http://example.com', timeout=1) as client:
        yield client


class TestHttpClient:
    root_url = 'http://example.com/'

    async def test_post_returns_ok_response(self, mock_aioresponse, http_client):
        mock_aioresponse.post(self.root_url, status=200, body='ok')
        response = await http_client.post('/')
        assert response.status == 200

    async def test_options_raises_http_error_on_timeout(
        self, mock_aioresponse, http_client
    ):
        mock_aioresponse.options(self.root_url, timeout=True)
        with pytest.raises(HttpError, match='Request failed OPTIONS'):
            await http_client.options('/')

    async def test_post_raises_http_error_on_unsuccessful_status(
        self,
        mock_aioresponse,
        http_client,
    ):
        mock_aioresponse.post(self.root_url, status=500)
        with pytest.raises(HttpError, match=r'Request failed POST'):
            await http_client.post('/')

    async def test_request_raises_when_client_is_not_started(self):
        client = HttpClient(base_url='http://example.com', timeout=1)
        with pytest.raises(RuntimeError, match='Session is not initialized'):
            await client.post('/')
