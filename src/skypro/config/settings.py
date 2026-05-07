from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

BASE_DIR = Path(__file__).resolve().parent.parent

HOME_PATH = Path.home() / '.skypro'
SETTINGS_FILE_PATH = HOME_PATH / 'settings.toml'


class SkyProSettings(BaseModel):
    email: str = ''
    password: str = ''


class Settings(BaseSettings):
    tax_percent: float = 6.0
    default_request_timeout: int = 3
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'

    skypro: SkyProSettings = Field(default_factory=SkyProSettings)

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        toml_file=SETTINGS_FILE_PATH,
        extra='ignore',
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            TomlConfigSettingsSource(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )

    @classmethod
    def from_toml_file(cls, file_path: Path) -> 'Settings':
        original_toml_file = cls.model_config.get('toml_file')
        cls.model_config['toml_file'] = file_path
        try:
            return cls()
        finally:
            cls.model_config['toml_file'] = original_toml_file


def _serialize_settings(current_settings: Settings) -> str:
    return _dump_toml(current_settings.model_dump())


def _dump_toml(data: dict[str, object]) -> str:
    root_lines: list[str] = []
    table_chunks: list[str] = []

    for key, value in data.items():
        if isinstance(value, dict):
            table_body = _dump_toml_table(value)
            table_chunks.append(f'[{key}]\n{table_body}')
            continue

        root_lines.append(f'{key} = {_format_toml_value(value)}')

    chunks = ['\n'.join(root_lines)] if root_lines else []
    chunks.extend(table_chunks)
    return '\n\n'.join(chunks) + '\n'


def _dump_toml_table(data: dict[str, object]) -> str:
    lines = [f'{key} = {_format_toml_value(value)}' for key, value in data.items()]
    return '\n'.join(lines)


def _format_toml_value(value: object) -> str:
    if isinstance(value, str):
        escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped_value}"'
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def get_default_settings() -> Settings:
    return Settings.model_construct(
        **{
            field_name: field_info.get_default(call_default_factory=True)
            for field_name, field_info in Settings.model_fields.items()
        }
    )


def save_settings(
    current_settings: Settings, file_path: Path = SETTINGS_FILE_PATH
) -> None:
    file_path.parent.mkdir(mode=0o700, exist_ok=True)
    file_path.write_text(_serialize_settings(current_settings), encoding='utf-8')


def ensure_settings_file(file_path: Path = SETTINGS_FILE_PATH) -> None:
    if file_path.exists():
        return

    save_settings(get_default_settings(), file_path)


def get_settings(file_path: Path = SETTINGS_FILE_PATH) -> Settings:
    file_path.parent.mkdir(mode=0o700, exist_ok=True)
    ensure_settings_file(file_path)
    return Settings.from_toml_file(file_path)


settings = get_settings()
