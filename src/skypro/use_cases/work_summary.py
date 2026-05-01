from calendar import monthrange
from datetime import date
from typing import TypedDict

from skypro.clients import SkyProClient
from skypro.config import settings
from skypro.utils.work_costs import WorkCost, WorkType, get_work_costs


class WorkSummary(TypedDict):
    type: WorkType
    count: int
    price: WorkCost
    total: float
    total_with_tax: float


async def get_work_summary(year: int, month: int) -> list[WorkSummary]:
    first_month_day = 1
    _, last_month_day = monthrange(year, month)

    async with SkyProClient() as client:
        account_data = await client.get_account_data(
            start_date=date(year, month, first_month_day),
            end_date=date(year, month, last_month_day),
        )

    work_costs = get_work_costs()
    works = account_data.services_summary.model_dump(by_alias=True)

    return [
        WorkSummary(
            type=work_type,
            count=works_count,
            price=work_costs[work_type],
            total=_calculate_total_price(
                work_costs[work_type], works_count, with_tax=False
            ),
            total_with_tax=_calculate_total_price(
                work_costs[work_type], works_count, with_tax=True
            ),
        )
        for work_type, works_count in works.items()
    ]


def _calculate_total_price(
    single_work_price: float, works_count: int, *, with_tax: bool
) -> float:
    total = works_count * single_work_price
    if with_tax:
        total = total * (100 - settings.tax_percent) / 100
    return round(total, 2)
