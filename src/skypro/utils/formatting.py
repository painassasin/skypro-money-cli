import locale


def format_price(price: float) -> str:
    return locale.currency(price, grouping=True)
