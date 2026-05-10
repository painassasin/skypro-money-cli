from functools import cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent.parent

HOME_DIR = Path.home() / '.skypro'

SETTINGS_FILE_PATH = HOME_DIR / 'settings.json'


class SkyProSettings(BaseModel):
    email: str
    password: str


class Settings(BaseSettings, json_file=SETTINGS_FILE_PATH, env_nested_delimiter='__'):
    tax_percent: float = 6.0
    default_request_timeout: int = 3

    skypro: SkyProSettings = Field(default_factory=SkyProSettings)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        env_settings: PydanticBaseSettingsSource,
        **_: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,
            JsonConfigSettingsSource(settings_cls),
        )


def save_settings(settings: Settings) -> None:
    SETTINGS_FILE_PATH.parent.mkdir(mode=0o700, exist_ok=True)
    data = settings.model_dump_json(ensure_ascii=False, indent=2)
    SETTINGS_FILE_PATH.write_text(data, encoding='utf-8')


@cache
def get_settings() -> Settings:
    return Settings()
