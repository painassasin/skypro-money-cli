from decimal import Decimal

from skypro.config import get_settings
from skypro.domain.errors import MissingWorkPriceError
from skypro.domain.models import WorkPrice, WorkReportItem, WorkSummary


def build_work_report(
    prices: list[WorkPrice], summaries: list[WorkSummary]
) -> list[WorkReportItem]:
    price_map = {work_price.work_type: work_price.price for work_price in prices}

    work_reports = []
    for summary in summaries:
        work_price = price_map.get(summary.work_type)
        if work_price is None:
            raise MissingWorkPriceError

        work_reports.append(
            WorkReportItem(
                work_type=summary.work_type,
                quantity=summary.quantity,
                price=work_price,
                total=work_price * summary.quantity,
            )
        )

    return work_reports


def calculate_total(report: list[WorkReportItem]) -> Decimal:
    return sum((item.total for item in report), Decimal(0))


def apply_tax(amount: Decimal) -> Decimal:
    tax_rate = Decimal(str(get_settings().tax_percent)) / Decimal(100)
    return amount * (Decimal(1) - tax_rate)
