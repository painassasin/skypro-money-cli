from datetime import date
from decimal import Decimal

import pytest

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkPrice, WorkReportItem, WorkSummary
from skypro.domain.services import settings as domain_settings
from skypro.use_cases import SummaryInfo, get_summary_info


@pytest.fixture
def work_prices() -> list[WorkPrice]:
    return [
        WorkPrice(WorkType.HOMEWORK, Decimal(100)),
        WorkPrice(WorkType.COURSEWORK, Decimal(200)),
    ]


@pytest.fixture
def work_summaries() -> list[WorkSummary]:
    return [
        WorkSummary(WorkType.HOMEWORK, 2),
        WorkSummary(WorkType.COURSEWORK, 3),
    ]


@pytest.fixture
def mocked_get_works_prices(mocker, work_prices):
    return mocker.patch(
        'skypro.use_cases.get_summary_info.get_works_prices', return_value=work_prices
    )


@pytest.fixture
def mocked_get_summary(mocker, work_summaries):
    return mocker.patch(
        'skypro.use_cases.get_summary_info.get_summary', return_value=work_summaries
    )


@pytest.fixture
def mocked_tax_percent(monkeypatch):
    monkeypatch.setattr(domain_settings, 'tax_percent', 6.0)


@pytest.mark.usefixtures('mocked_tax_percent')
async def test_get_summary_info_returns_report_totals_and_tax(
    mocked_get_works_prices,
    mocked_get_summary,
) -> None:
    summary_info = await get_summary_info(2026, 1)

    mocked_get_works_prices.assert_called_once()
    mocked_get_summary.assert_awaited_once_with(date(2026, 1, 1), date(2026, 1, 31))

    assert summary_info == SummaryInfo(
        report=[
            WorkReportItem(WorkType.HOMEWORK, 2, Decimal(100), Decimal(200)),
            WorkReportItem(WorkType.COURSEWORK, 3, Decimal(200), Decimal(600)),
        ],
        total=Decimal(800),
        total_after_tax=Decimal('752.00'),
    )
