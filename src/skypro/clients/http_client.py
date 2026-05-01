import logging
from types import TracebackType
from typing import Any, Self

from aiohttp import (
    ClientError,
    ClientResponse,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
)

from .errors import HttpError

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url: str, timeout: int) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self.__session: ClientSession | None = None

    async def __aenter__(self) -> Self:
        self.__session = ClientSession(
            base_url=self._base_url, timeout=ClientTimeout(total=self._timeout)
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        if self.__session:
            await self.__session.close()
            self.__session = None

    async def options(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self._request('OPTIONS', url, **kwargs)

    async def get(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self._request('GET', url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> ClientResponse:
        return await self._request('POST', url, **kwargs)

    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> ClientResponse:
        logger.info('HTTP request: %s %s', method, url)

        try:
            response = await self._session.request(method, url, **kwargs)
            response.raise_for_status()
        except ClientResponseError as e:
            raise HttpError(f'HTTP {e.status}: {method} {url}') from e
        except (ClientError, TimeoutError) as e:
            raise HttpError(f'Network error: {method} {url}') from e
        else:
            logger.info('HTTP response: %s %s -> %s', method, url, response.status)
            return response

    @property
    def _session(self) -> ClientSession:
        if self.__session is None or self.__session.closed:
            raise RuntimeError('Session is not initialized or already closed')
        return self.__session
