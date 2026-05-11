import asyncio
import json

import typer
from rich.console import Console
from typer import Option

from skypro.config import (
    configure_skypro_settings,
    enable_console_logging,
    get_settings,
    is_skypro_configured,
)

from . import commands

app = typer.Typer()
console = Console()


@app.command(name='summary')
def get_summary(
    year: int | None = Option(None, help='Год для расчета'),
    month: int | None = Option(None, help='Месяц для расчета'),
    verbose: bool = typer.Option(False, '-v', '--verbose'),
) -> None:
    """Расчет стоимости работ"""
    if not is_skypro_configured():
        console.print(
            '[red]Настройки SkyPro не заданы. '
            'Укажите их командой `sky-cli config --skypro`.[/]'
        )
        raise typer.Exit(code=1)

    if verbose:
        enable_console_logging(console)

    asyncio.run(commands.show_summary(console, year, month))


@app.command(name='config')
def configure(
    skypro: bool = Option(
        False,
        '--skypro',
        help='Изменить настройки доступа к SkyPro',
    ),
) -> None:
    """Просмотр текущего конфига или настройка доступа к SkyPro"""
    if skypro:
        configure_skypro_settings(console)
        return

    settings = get_settings().model_dump(mode='json')
    console.print(json.dumps(settings, ensure_ascii=False, indent=2))
