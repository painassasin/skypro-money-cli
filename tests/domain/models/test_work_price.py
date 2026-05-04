from decimal import Decimal

import pytest

from skypro.domain.errors import InvalidPriceError
from skypro.domain.models import WorkPrice


def test_work_price_should_be_greater_then_zero(work_type) -> None:
    work_price = WorkPrice(work_type=work_type, price=Decimal(100))
    assert work_price.work_type is work_type
    assert work_price.price == Decimal(100)


@pytest.mark.parametrize(
    'invalid_price', [Decimal(0), Decimal(-1)], ids=['zero', 'negative']
)
def test_invalid_price(work_type, invalid_price: Decimal) -> None:
    with pytest.raises(InvalidPriceError):
        WorkPrice(work_type=work_type, price=invalid_price)
