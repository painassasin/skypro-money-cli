import logging
from types import TracebackType
from typing import Any, Self

import httpx
from httpx import AsyncClient, Request, Response

from skypro.config import get_settings

from .errors import HttpError

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, timeout: int | None = None) -> None:
        self._client = AsyncClient(
            timeout=timeout or get_settings().default_request_timeout,
            follow_redirects=True,
            event_hooks={'request': [_log_request], 'response': [_log_response]},
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.aclose()

    @property
    def client(self) -> AsyncClient:
        return self._client

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        try:
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HttpError(f'HTTP {e.response.status_code}: {method} {url}') from e
        except httpx.HTTPError as e:
            raise HttpError(f'Network error: {method} {url}') from e
        else:
            return response


async def _log_request(request: Request) -> None:  # ruff:ignore[unused-async]
    logger.info(
        'HTTP request: %s %s',
        request.method,
        request.url,
    )


async def _log_response(response: Response) -> None:  # ruff:ignore[unused-async]
    logger.info(
        'HTTP response: %s %s -> %s',
        response.request.method,
        response.request.url,
        response.status_code,
    )
