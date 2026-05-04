import asyncio
from asyncio import gather
from datetime import date
from decimal import Decimal
from typing import NamedTuple

from skypro.domain.models import WorkReportItem
from skypro.domain.services import apply_tax, build_work_report, calculate_total
from skypro.infra.repositories import get_summary, get_works_prices


class SummaryInfo(NamedTuple):
    report: list[WorkReportItem]
    total: Decimal
    total_after_tax: Decimal


async def get_summary_info(start_date: date, end_date: date) -> SummaryInfo:
    work_prices, work_summaries = await gather(
        asyncio.to_thread(get_works_prices),
        get_summary(start_date, end_date),
    )

    report = build_work_report(work_prices, work_summaries)
    total = calculate_total(report)
    total_after_tax = apply_tax(total)

    return SummaryInfo(report, total, total_after_tax)
