from calendar import IllegalMonthError
from datetime import UTC, datetime

from click.exceptions import Exit
from rich.console import Console

from skypro.cli.renders import render_summary_table
from skypro.domain.errors import DomainError
from skypro.infra.repositories.errors import RepositoryError
from skypro.use_cases import get_summary_info


async def show_summary(
    console: Console,
    year: int | None,
    month: int | None,
) -> None:
    now = datetime.now(UTC).astimezone()
    year = year or now.year
    month = month or now.month

    try:
        with console.status('[cyan]Расчет стоимости работ'):
            report, total, after_tax = await get_summary_info(year, month)

        table = render_summary_table(report, total, after_tax)
        console.print(table)
    except (RepositoryError, DomainError, IllegalMonthError) as e:
        console.print(f'[bold red]Error: {e!s}[/]')
        raise Exit(code=1) from e
