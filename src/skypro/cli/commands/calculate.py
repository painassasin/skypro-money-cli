from collections.abc import Iterable
from datetime import UTC, datetime

from rich.console import Console
from rich.table import Column, Table

from skypro.api.http.client import HttpClient
from skypro.api.skypro.client import SkyProClient
from skypro.services import calculate_total_price, get_work_summary
from skypro.services.dto import WorkSummary
from skypro.utils import format_price, get_month_range


async def calculate_command(
    console: Console,
    year: int | None,
    month: int | None,
) -> None:
    now = datetime.now(UTC).astimezone()
    target_year = year or now.year
    target_month = month or now.month

    start, end = get_month_range(target_year, target_month)

    async with HttpClient() as client:
        skypro = SkyProClient(client)
        work_summary = await get_work_summary(skypro, start, end)

    table = build_work_summary_table(work_summary)

    console.print(table)


def build_work_summary_table(work_summary: Iterable[WorkSummary]) -> Table:
    table = Table(
        Column('Work Type', style='cyan'),
        Column('Count', style='magenta'),
        Column('Amount', style='magenta', justify='right'),
        title='Mentor Statistics',
    )

    for work in work_summary:
        if not work['works_count']:
            continue
        table.add_row(
            work['work_type'],
            str(work['works_count']),
            format_price(work['total_price']),
        )

    total = calculate_total_price(work_summary)
    total_with_tax = calculate_total_price(work_summary, with_tax=True)
    table.add_section()
    table.add_row('Total', '', format_price(total))
    table.add_row('Total amount', '', format_price(total_with_tax))

    return table
