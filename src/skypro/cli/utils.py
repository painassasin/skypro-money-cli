import os

from rich.console import Console

from skypro.config import get_settings, save_settings


def set_skypro_settings(console: Console) -> None:
    console.print('Укажи настройки SkyPro')
    os.environ['SKYPRO__EMAIL'] = console.input('Email: ')
    os.environ['SKYPRO__PASSWORD'] = console.input('Password: ', password=True)
    get_settings.cache_clear()
    new_settings = get_settings()
    save_settings(new_settings)
