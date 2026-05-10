import locale
import os
import random
from collections.abc import AsyncIterator

import pytest

from skypro.config import get_settings
from skypro.domain.enums import WorkType
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.http.client import HttpClient


@pytest.fixture(autouse=True, scope='session')
def settings():
    get_settings.cache_clear()
    os.environ['SKYPRO__EMAIL'] = 'mentor@example.com'
    os.environ['SKYPRO__PASSWORD'] = 'secret-password'
    return get_settings()


@pytest.fixture(autouse=True, scope='session')
def activate_rus_locale():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


@pytest.fixture
def work_type() -> WorkType:
    return random.choice(list(WorkType))


@pytest.fixture
async def http_client() -> AsyncIterator[HttpClient]:
    async with HttpClient() as client:
        yield client


@pytest.fixture
def skypro_client(http_client: HttpClient) -> SkyProClient:
    return SkyProClient(http_client)
