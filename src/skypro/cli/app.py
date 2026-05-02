import asyncio
from calendar import IllegalMonthError

import typer
from click.exceptions import Exit
from rich.console import Console
from typer import Option

from skypro.api.http.errors import HttpError
from skypro.api.skypro.errors import AuthenticationError
from skypro.cli import commands

app = typer.Typer()
console = Console()


@app.command(name='statistics')
def show_statistic(
    year: int | None = Option(None, help='Год для расчета'),
    month: int | None = Option(None, help='Месяц для расчета'),
) -> None:
    """Расчет стоимости работ"""
    with console.status('[cyan]Расчет стоимости работ'):
        try:
            asyncio.run(
                commands.show_statistics(console=console, year=year, month=month)
            )
        except (HttpError, AuthenticationError, IllegalMonthError) as e:
            console.print(f'[bold red]Error: {e!s}[/]')
            raise Exit(code=1) from e
