from decimal import Decimal

import pytest

from skypro.domain.enums import WorkType
from skypro.domain.errors import MissingWorkPriceError
from skypro.domain.models import WorkPrice, WorkReportItem, WorkSummary
from skypro.domain.services import build_work_report


def test_build_work_report_returns_report_items():
    prices = [
        WorkPrice(work_type=WorkType.HOMEWORK, price=Decimal(100)),
        WorkPrice(work_type=WorkType.COURSEWORK, price=Decimal(250)),
    ]
    summaries = [
        WorkSummary(work_type=WorkType.HOMEWORK, quantity=2),
        WorkSummary(work_type=WorkType.COURSEWORK, quantity=3),
    ]

    report = build_work_report(prices=prices, summaries=summaries)

    assert report == [
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


def test_build_work_report_raises_error_when_price_missing():
    prices = [WorkPrice(work_type=WorkType.HOMEWORK, price=Decimal(100))]
    summaries = [WorkSummary(work_type=WorkType.DIPLOMA, quantity=1)]

    with pytest.raises(MissingWorkPriceError):
        build_work_report(prices=prices, summaries=summaries)
