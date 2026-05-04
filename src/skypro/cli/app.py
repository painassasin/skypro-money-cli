import asyncio

import typer
from rich.console import Console
from typer import Option

from . import commands

app = typer.Typer()
console = Console()


@app.command(name='summary')
def get_summary(
    year: int | None = Option(None, help='Год для расчета'),
    month: int | None = Option(None, help='Месяц для расчета'),
) -> None:
    """Расчет стоимости работ"""
    asyncio.run(commands.show_summary(console, year, month))
