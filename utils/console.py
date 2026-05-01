import locale


def format_price(price: float) -> str:
    return locale.currency(price, symbol=True, grouping=True)
