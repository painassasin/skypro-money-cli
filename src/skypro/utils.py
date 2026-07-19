import locale
from calendar import monthrange
from datetime import date
from decimal import Decimal


def get_month_range(year: int, month: int) -> tuple[date, date]:
    first_day = 1
    _, last_day = monthrange(year, month)
    return date(year, month, first_day), date(year, month, last_day)


def format_price(price: Decimal) -> str:
    try:
        return locale.currency(price, grouping=True)
    except locale.Error:
        return f'{price:,.2f}'
