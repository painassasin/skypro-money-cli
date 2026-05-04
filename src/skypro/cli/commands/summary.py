from calendar import IllegalMonthError
from datetime import UTC, date, datetime

from click.exceptions import Exit
from rich.console import Console

from skypro.cli.renders import render_summary_table
from skypro.domain.errors import DomainError
from skypro.infra.repositories.errors import RepositoryError
from skypro.use_cases import get_summary_info
from skypro.utils import get_month_range


async def show_summary(
    console: Console,
    year: int | None,
    month: int | None,
) -> None:
    try:
        start, end = resolve_period(year, month)

        with console.status('[cyan]Расчет стоимости работ'):
            report, total, after_tax = await get_summary_info(start, end)

        table = render_summary_table(report, total, after_tax)
        console.print(table)
    except (RepositoryError, DomainError, IllegalMonthError) as e:
        console.print(f'[bold red]Error: {e!s}[/]')
        raise Exit(code=1) from e


def resolve_period(year: int | None, month: int | None) -> tuple[date, date]:
    now = datetime.now(UTC).astimezone()
    target_year = year or now.year
    target_month = month or now.month

    start, end = get_month_range(target_year, target_month)
    return start, end
