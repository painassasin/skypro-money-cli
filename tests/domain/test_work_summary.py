import pytest

from skypro.domain.errors import InvalidQuantityError
from skypro.domain.models import WorkSummary


@pytest.mark.parametrize('quantity', [0, 1], ids=['zero', 'positive'])
def test_work_quantity_should_be_greater_or_equal_zero(work_type, quantity):
    work_summary = WorkSummary(work_type=work_type, quantity=quantity)
    assert work_summary.work_type is work_type
    assert work_summary.quantity == quantity


def test_work_quantity_failed_to_be_negative(work_type):
    with pytest.raises(InvalidQuantityError):
        WorkSummary(work_type=work_type, quantity=-10)
