import random
from datetime import date
from decimal import Decimal

import click
import pytest
from freezegun import freeze_time
from rich.console import Console

from skypro.cli.commands.summary import show_summary
from skypro.domain.enums import WorkType
from skypro.domain.models import WorkReportItem
from skypro.use_cases import SummaryInfo


@pytest.fixture
def console(mocker):
    return mocker.MagicMock(spec=Console)


@pytest.fixture
def report() -> list[WorkReportItem]:
    return [
        WorkReportItem(WorkType.HOMEWORK, 2, Decimal(100), Decimal(200)),
        WorkReportItem(WorkType.COURSEWORK, 3, Decimal(250), Decimal(750)),
    ]


@pytest.fixture
def mocked_get_summary_info(mocker, report):
    mock = mocker.patch('skypro.cli.commands.summary.get_summary_info')
    mock.return_value = SummaryInfo(
        report=report, total=Decimal(950), total_after_tax=Decimal(800)
    )
    return mock


@freeze_time('2026-03-02')
async def test_correctly_get_current_month_if_not_set(mocked_get_summary_info, console):
    await show_summary(console, None, None)
    mocked_get_summary_info.assert_awaited_once_with(
        date(2026, 3, 1), date(2026, 3, 31)
    )


@pytest.mark.usefixtures('mocked_get_summary_info')
async def test_exit_if_set_invalid_month(console):
    invalid_month_number = random.randrange(13, 20)

    with pytest.raises(click.exceptions.Exit) as exc_info:
        await show_summary(console, None, invalid_month_number)

    assert exc_info.value.exit_code == 1
    console.print.assert_called_once_with(
        f'[bold red]Error: bad month number {invalid_month_number}; must be 1-12[/]'
    )
