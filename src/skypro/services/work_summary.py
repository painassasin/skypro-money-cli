from datetime import date

from skypro.api.skypro.client import SkyProClient
from skypro.config.work_costs import load_work_costs
from skypro.services.dto import WorkSummary


async def get_work_summary(
    client: SkyProClient,
    start_date: date,
    end_date: date,
) -> list[WorkSummary]:
    work_costs = load_work_costs()

    data = await client.get_account_data(start_date, end_date)
    summary = data.services_summary

    return [
        WorkSummary(
            work_type=work_type,
            works_count=works_count,
            total_price=float(works_count * work_costs[work_type]),
        )
        for work_type, works_count in summary.model_dump(by_alias=True).items()
    ]
