import locale
from decimal import Decimal


def format_price(price: Decimal | float) -> str:
    return locale.currency(price, grouping=True)
