import asyncio

import typer
from click.exceptions import Exit
from rich.console import Console
from typer import Option

from skypro.api.http.errors import HttpError
from skypro.api.skypro.errors import AuthenticationError
from skypro.cli.commands import calculate_command

app = typer.Typer(help='Skypro mentor app')
console = Console()


@app.command()
def calculate(
    year: int | None = Option(None, help='Year to calculate'),
    month: int | None = Option(None, help='Month to calculate'),
) -> None:
    """Calculate work costs"""
    with console.status('[cyan]Calculate work costs'):
        try:
            asyncio.run(calculate_command(console=console, year=year, month=month))
        except (HttpError, AuthenticationError) as e:
            console.print(f'[bold red]Error: {e!s}[/]')
            raise Exit(code=1) from e
