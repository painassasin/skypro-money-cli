import json
from functools import cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent.parent

HOME_DIR = Path.home() / '.skypro'

SETTINGS_FILE_PATH = HOME_DIR / 'settings.json'


class SkyProSettings(BaseModel):
    email: str | None = None
    password: SecretStr | None = None


class Settings(BaseSettings, json_file=SETTINGS_FILE_PATH):
    tax_percent: float = 6.0
    default_request_timeout: int = 3
    log_level: Literal['debug', 'info'] = 'info'

    skypro: SkyProSettings = Field(default_factory=SkyProSettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **_: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)


def save_settings(settings: Settings) -> None:
    SETTINGS_FILE_PATH.parent.mkdir(mode=0o700, exist_ok=True)

    data = settings.model_dump(mode='json')
    data['skypro']['password'] = settings.skypro.password.get_secret_value()

    with SETTINGS_FILE_PATH.open(mode='w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    get_settings.cache_clear()


@cache
def get_settings() -> Settings:
    return Settings()
