import asyncio

import typer
from pydantic import ValidationError
from rich.console import Console
from typer import Option

from skypro.config import enable_console_logging, get_settings

from . import commands
from .utils import set_skypro_settings

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


@app.callback()
def check_settings() -> None:
    try:
        get_settings()
    except ValidationError:
        set_skypro_settings(console)
