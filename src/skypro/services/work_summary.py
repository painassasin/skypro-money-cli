from datetime import date
from decimal import Decimal

from skypro.api.skypro.client import SkyProClient
from skypro.domain import WorkItem, WorkType
from skypro.repositories import load_work_costs


async def get_work_summary(
    client: SkyProClient,
    start_date: date,
    end_date: date,
) -> list[WorkItem]:
    work_costs = load_work_costs()

    data = await client.get_account_data(start_date, end_date)

    return [
        WorkItem(
            type=WorkType.HOMEWORK,
            count=data.services_summary.homework,
            unit_price=Decimal(work_costs['ДЗ']),
        ),
        WorkItem(
            type=WorkType.COURSEWORK,
            count=data.services_summary.coursework,
            unit_price=Decimal(work_costs['КР']),
        ),
        WorkItem(
            type=WorkType.DIPLOMA,
            count=data.services_summary.diploma,
            unit_price=Decimal(work_costs['ДР']),
        ),
        WorkItem(
            type=WorkType.LIVE,
            count=data.services_summary.live,
            unit_price=Decimal(work_costs['Лайв']),
        ),
        WorkItem(
            type=WorkType.CONSULTATION,
            count=data.services_summary.individual_consultation,
            unit_price=Decimal(work_costs['ИК']),
        ),
    ]
