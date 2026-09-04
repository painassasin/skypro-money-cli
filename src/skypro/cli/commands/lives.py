from calendar import IllegalMonthError
from datetime import UTC, datetime

import typer
from rich.console import Console

from skypro.cli.renders import render_lives_table
from skypro.domain.errors import DomainError
from skypro.infra.repositories.errors import RepositoryError
from skypro.use_cases import get_lives_info


async def show_lives_info(
    console: Console,
    year: int | None,
    month: int | None,
) -> None:
    now = datetime.now(UTC).astimezone()
    year = year or now.year
    month = month or now.month

    try:
        with console.status('[cyan]Получение информации'):
            lives = await get_lives_info(year, month)
    except (RepositoryError, DomainError, IllegalMonthError) as e:
        console.print(f'[bold red]Error: {e!s}[/]')
        raise typer.Exit(code=1) from e

    if not lives:
        console.print(f'No lives for {year}/{month}')
        return

    table = render_lives_table(*lives)
    console.print(table)
