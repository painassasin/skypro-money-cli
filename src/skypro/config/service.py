from pydantic import SecretStr
from rich.console import Console

from .settings import Settings, get_settings, save_settings


def is_skypro_configured(settings: Settings | None = None) -> bool:
    current_settings = settings or get_settings()
    return bool(current_settings.skypro.email and current_settings.skypro.password)


def configure_skypro_settings(console: Console) -> Settings:
    current_settings = get_settings()

    console.print('[cyan]Настройка доступа к SkyPro[/]')

    current_email = current_settings.skypro.email or ''
    email_prompt = 'Email'
    if current_email:
        email_prompt = f'Email [{current_email}]'

    email = console.input(f'{email_prompt}: ').strip() or current_email
    password = console.input('Password: ', password=True).strip()
    if not password and current_settings.skypro.password:
        password = current_settings.skypro.password_value

    updated_settings = current_settings.model_copy(
        update={
            'skypro': current_settings.skypro.model_copy(
                update={'email': email, 'password': SecretStr(password)}
            )
        }
    )
    save_settings(updated_settings)
    return updated_settings


def ensure_skypro_configured(console: Console) -> Settings:
    settings = get_settings()
    if is_skypro_configured(settings):
        return settings

    console.print('[yellow]Конфигурация SkyPro не найдена. Заполним ее сейчас.[/]')
    return configure_skypro_settings(console)
