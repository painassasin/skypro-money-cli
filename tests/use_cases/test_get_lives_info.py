from datetime import UTC, date, datetime

import pytest

from skypro.domain.models import Live
from skypro.use_cases import get_lives_info


@pytest.fixture
def mocked_get_lives(mocker):
    return mocker.patch('skypro.use_cases.get_lives_info.get_lives')


@pytest.mark.parametrize(
    ('year', 'month', 'start_date', 'end_date'),
    [
        (2026, 1, date(2026, 1, 1), date(2026, 1, 31)),
        (2024, 2, date(2024, 2, 1), date(2024, 2, 29)),
    ],
)
async def test_get_lives_info_requests_lives_for_month(
    mocked_get_lives, year, month, start_date, end_date
) -> None:
    lives = [Live('Python', datetime(2026, 1, 10, 12, 0, tzinfo=UTC))]
    mocked_get_lives.return_value = lives

    result = await get_lives_info(year, month)

    mocked_get_lives.assert_awaited_once_with(start_date, end_date)
    assert result is lives
