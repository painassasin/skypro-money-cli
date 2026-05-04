from typing import Any
from urllib.parse import urljoin

from httpx import Cookies, Response

from skypro.infra.http.client import HttpClient


class BaseApiClient:
    base_url: str

    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client

    @property
    def cookies(self) -> Cookies:
        return self._http.client.cookies

    async def _get(self, url: str, **kwargs: Any) -> Response:
        return await self._request('GET', url, **kwargs)

    async def _post(self, url: str, **kwargs: Any) -> Response:
        return await self._request('POST', url, **kwargs)

    async def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        return await self._http.request(
            method=method, url=self._build_url(path), **kwargs
        )

    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path)
