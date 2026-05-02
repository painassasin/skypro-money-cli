from calendar import IllegalMonthError
from datetime import date

import pytest

from skypro.utils.dates import get_month_range


@pytest.mark.parametrize(
    ('year', 'month', 'expected_start', 'expected_end'),
    [
        (2026, 1, date(2026, 1, 1), date(2026, 1, 31)),
        (2026, 4, date(2026, 4, 1), date(2026, 4, 30)),
        (2024, 2, date(2024, 2, 1), date(2024, 2, 29)),
    ],
)
def test_get_month_range_returns_first_and_last_day(
    year, month, expected_start, expected_end
):
    assert get_month_range(year, month) == (expected_start, expected_end)


def test_get_month_range_raises_for_invalid_month():
    with pytest.raises(IllegalMonthError):
        get_month_range(2026, 13)
