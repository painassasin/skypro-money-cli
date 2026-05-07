import asyncio

import typer
from rich.console import Console
from typer import Option

from skypro.config.logging import enable_console_logging

from . import commands
from .commands import initialize_settings

app = typer.Typer()
console = Console()


@app.command(name='summary')
def get_summary(
    year: int | None = Option(None, help='Год для расчета'),
    month: int | None = Option(None, help='Месяц для расчета'),
    *,
    verbose: bool = typer.Option(False, '-v', '--verbose'),  # noqa: FBT003
) -> None:
    """Расчет стоимости работ"""
    if verbose:
        enable_console_logging(console)
    asyncio.run(commands.show_summary(console, year, month))


@app.command(name='init')
def init_settings() -> None:
    """Установка настроек."""
    asyncio.run(initialize_settings(console))
    console.print('[green]OK[/]')
