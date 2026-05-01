from collections.abc import Iterable
from operator import itemgetter

from skypro.config.settings import settings
from skypro.services.dto import WorkSummary


def calculate_total_price(
    work_summary: Iterable[WorkSummary], *, with_tax: bool = False
) -> float:
    total = sum(map(itemgetter('total_price'), work_summary))
    if with_tax:
        total *= (100 - settings.tax_percent) / 100
    return float(total)
