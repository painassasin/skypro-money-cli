from decimal import Decimal

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkReportItem
from skypro.domain.services import calculate_total


def test_calculate_total_returns_sum_of_report_items():
    report = [
        WorkReportItem(
            work_type=WorkType.HOMEWORK,
            quantity=2,
            price=Decimal(100),
            total=Decimal(200),
        ),
        WorkReportItem(
            work_type=WorkType.COURSEWORK,
            quantity=3,
            price=Decimal(250),
            total=Decimal(750),
        ),
    ]

    total = calculate_total(report)

    assert total == Decimal(950)


def test_calculate_total_returns_zero_for_empty_report():
    assert calculate_total([]) == Decimal(0)
