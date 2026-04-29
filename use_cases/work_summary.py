from calendar import monthrange
from datetime import date
from typing import TypedDict

from clients import SkyProClient
from utils.work_costs import WorkType, WorkCost, get_work_costs


class WorkSummary(TypedDict):
    work_type: WorkType
    count: int
    price: WorkCost
    total: int


async def get_work_summary(year: int, month: int) -> list[WorkSummary]:
    first_month_day = 1
    _, last_month_day = monthrange(year, month)

    async with SkyProClient() as client:
        account_data = await client.get_account_data(
            start_date=date(year, month, first_month_day),
            end_date=date(year, month, last_month_day)
        )

    work_costs = get_work_costs()
    works = account_data.services_summary.model_dump(by_alias=True)
    return [
        WorkSummary(
            work_type=work_type,
            count=works_count,
            price=work_costs[work_type],
            total=work_costs[work_type] * works_count,
        )
        for work_type, works_count in works.items()
    ]
