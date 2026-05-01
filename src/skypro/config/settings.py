from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class SkyProSettings(BaseModel):
    email: str
    password: str


class Settings(BaseSettings):
    tax_percent: float = 6.0
    default_request_timeout: int = 3
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'

    skypro: SkyProSettings = Field(default_factory=SkyProSettings)

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_file='.env',
        extra='ignore',
    )


settings = Settings()
