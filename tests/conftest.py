import locale
import random
from collections.abc import AsyncIterator

import pytest
from pydantic import SecretStr
from rich.console import Console

from skypro.config import get_settings, save_settings
from skypro.config.settings import SETTINGS_FILE_PATH, Settings
from skypro.domain.enums import WorkType
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.http.client import HttpClient


@pytest.fixture(autouse=True)
def settings(tmp_path, monkeypatch):
    settings_path = tmp_path / 'settings.json'
    monkeypatch.setattr('skypro.config.settings.SETTINGS_FILE_PATH', settings_path)
    Settings.model_config['json_file'] = settings_path
    get_settings.cache_clear()

    configured_settings = Settings()
    configured_settings.skypro.email = 'mentor@example.com'
    configured_settings.skypro.password = SecretStr('secret-password')
    save_settings(configured_settings)

    yield get_settings()

    get_settings.cache_clear()
    Settings.model_config['json_file'] = SETTINGS_FILE_PATH


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


@pytest.fixture
def console(mocker):
    return mocker.Mock(spec=Console)
