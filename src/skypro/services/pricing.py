from collections.abc import Iterable
from decimal import Decimal

from skypro.config.settings import settings
from skypro.domain import WorkItem


def calculate_total_price(
    work_summary: Iterable[WorkItem], *, with_tax: bool = False
) -> Decimal:
    total = sum((work.total_price for work in work_summary), start=Decimal())
    if with_tax:
        total *= (Decimal(100) - Decimal(str(settings.tax_percent))) / Decimal(100)
    return total
