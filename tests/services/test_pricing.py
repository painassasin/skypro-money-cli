from decimal import Decimal

import pytest

from skypro.config.settings import settings
from skypro.domain import WorkItem, WorkType
from skypro.services.pricing import calculate_total_price


@pytest.fixture
def work_summary():
    return [
        WorkItem(type=WorkType.HOMEWORK, count=2, unit_price=Decimal(100)),
        WorkItem(type=WorkType.LIVE, count=3, unit_price=Decimal('250.50')),
    ]


def test_calculate_total_price_returns_sum_without_tax(work_summary):
    result = calculate_total_price(work_summary)
    assert result == Decimal('951.50')


def test_calculate_total_price_applies_tax_percent_from_settings(work_summary, mocker):
    mocker.patch.object(settings, 'tax_percent', 6.0)
    result = calculate_total_price(work_summary, with_tax=True)
    assert result == Decimal('894.41')


def test_calculate_total_price_returns_zero_for_empty_work_summary():
    result = calculate_total_price([])
    assert result == Decimal() == 0
