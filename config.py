from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path.cwd()


class SkyPro(BaseModel):
    email: str
    password: str
    base_url: str = 'https://operation-planning.sky.pro'


class Settings(BaseSettings):
    tax_percent: float = 6.0

    skypro: SkyPro = Field(default_factory=SkyPro)

    model_config = SettingsConfigDict(
        env_nested_delimiter='__', env_file=BASE_DIR / '.env'
    )


settings = Settings()
