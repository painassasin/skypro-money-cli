import asyncio
import locale
import operator
from datetime import UTC, datetime

from click.exceptions import Exit
from rich.console import Console
from rich.table import Column, Table
from typer import Option, Typer

from clients.errors import SkyProError
from use_cases import get_work_summary
from use_cases.work_summary import WorkSummary
from utils import format_price

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = Typer(help='SkyPro Mentor Statistics Calculator')
console = Console()


@app.command()
def calculate(
    year: int | None = Option(None, help='Year to calculate'),
    month: int | None = Option(None, help='Month to calculate'),
) -> None:
    """Calculate work costs"""
    now = datetime.now(UTC).astimezone()
    target_year = year or now.year
    target_month = month or now.month

    try:
        work_summary = asyncio.run(get_work_summary(target_year, target_month))
    except SkyProError as e:
        console.print(f'[bold red]Error: {e!s}[/]')
        raise Exit(code=1) from e

    _print_summary_table(target_year, target_month, *work_summary)


def _print_summary_table(year: int, month: int, *work_summary: WorkSummary) -> None:
    if not sum(map(operator.itemgetter('count'), work_summary)):
        console.print('No work done yet', style='cyan')
        return

    table = Table(
        Column('Work type', style='cyan'),
        Column('Count', style='magenta', justify='center'),
        Column('Price', style='magenta', justify='right'),
        title=f'Statistics for {year}/{month}',
    )
    for work in work_summary:
        if not work['count']:
            continue

        table.add_row(work['type'], str(work['count']), format_price(work['total']))

    table.add_section()
    total_price = sum(map(operator.itemgetter('total'), work_summary))
    total_price_with_tax = sum(map(operator.itemgetter('total_with_tax'), work_summary))
    table.add_row('Total', '', format_price(total_price))
    table.add_row('Total amount', '', format_price(total_price_with_tax))
    console.print(table)


if __name__ == '__main__':
    app()
