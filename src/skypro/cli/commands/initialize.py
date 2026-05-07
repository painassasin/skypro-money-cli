from rich.console import Console

from skypro.config.settings import save_settings, settings
from skypro.infra.api.errors import ApiError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.http.client import HttpClient
from skypro.infra.http.errors import HttpError


async def initialize_settings(console: Console) -> None:
    while not await is_skypro_credentials_valid():
        if settings.skypro.email:
            console.print('[red]Некорретные данные для skypro[/]')
        else:
            console.print('Укажи данные для подключения к skypro')

        _set_skypro_settings(console)


async def is_skypro_credentials_valid() -> bool:
    try:
        async with HttpClient() as http_client:
            skypro = SkyProClient(http_client)
            await skypro.login()
    except (HttpError, ApiError):
        return False

    return True


def _set_skypro_settings(console: Console) -> None:
    email = console.input('Email: ')
    password = console.input('Password: ', password=True)
    settings.skypro.email = email
    settings.skypro.password = password
    save_settings(settings)
