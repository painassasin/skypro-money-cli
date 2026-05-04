import json
from decimal import Decimal, InvalidOperation

from skypro.config.settings import BASE_DIR
from skypro.domain.enums import WorkType
from skypro.domain.models import WorkPrice

from .errors import PriceLoadError


def get_works_prices() -> list[WorkPrice]:
    try:
        with (BASE_DIR / 'work_prices.json').open() as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise PriceLoadError from e

    if not isinstance(data, dict):
        raise PriceLoadError

    try:
        return [
            WorkPrice(work_type=WorkType(work_type), price=Decimal(str(price)))
            for work_type, price in data.items()
        ]
    except (ValueError, InvalidOperation) as e:
        raise PriceLoadError from e
