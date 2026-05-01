import locale


def format_price(price: float) -> str:
    if isinstance(price, int):
        price = float(price)
    return locale.currency(price, symbol=True, grouping=True)
