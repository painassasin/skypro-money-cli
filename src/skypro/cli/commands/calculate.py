from datetime import UTC, date, datetime

from rich.console import Console
from rich.table import Column, Table

from skypro.api.http.client import HttpClient
from skypro.api.skypro.client import SkyProClient
from skypro.domain import WorkItem
from skypro.services import calculate_total_price, get_work_summary
from skypro.utils import format_price, get_month_range


async def calculate_command(
    console: Console,
    year: int | None,
    month: int | None,
) -> None:
    start, end = resolve_period(year, month)

    async with HttpClient() as client:
        skypro = SkyProClient(client)
        work_summary = await get_work_summary(skypro, start, end)

    table = build_work_summary_table(work_summary)

    console.print(table)


def resolve_period(year: int | None, month: int | None) -> tuple[date, date]:
    now = datetime.now(UTC).astimezone()
    target_year = year or now.year
    target_month = month or now.month

    start, end = get_month_range(target_year, target_month)
    return start, end


def build_work_summary_table(work_summary: list[WorkItem]) -> Table:
    table = Table(
        Column('Work Type', style='cyan'),
        Column('Count', style='magenta'),
        Column('Amount', style='magenta', justify='right'),
        title='Mentor Statistics',
    )

    for work in work_summary:
        if not work.count:
            continue

        table.add_row(
            work.type.value,
            str(work.count),
            format_price(work.total_price),
        )

    total = calculate_total_price(work_summary)
    total_with_tax = calculate_total_price(work_summary, with_tax=True)
    table.add_section()
    table.add_row('Total', '', format_price(total))
    table.add_row('Total amount', '', format_price(total_with_tax))

    return table
