from calendar import monthrange
from datetime import date


def get_month_range(year: int, month: int) -> tuple[date, date]:
    first_day = 1
    _, last_day = monthrange(year, month)
    return date(year, month, first_day), date(year, month, last_day)
