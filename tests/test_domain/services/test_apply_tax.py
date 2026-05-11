from decimal import Decimal

import pytest

from skypro.domain.services import apply_tax


@pytest.mark.parametrize(
    ('tax_percent', 'expected_amount'),
    [(6.0, Decimal('940.00')), (13.0, Decimal('870.00'))],
)
def test_apply_tax_returns_amount_with_tax_deduction(tax_percent, expected_amount):
    amount_with_tax = apply_tax(Decimal(1000), tax_percent)
    assert amount_with_tax == expected_amount
