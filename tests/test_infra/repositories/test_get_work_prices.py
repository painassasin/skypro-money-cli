import json
from decimal import Decimal
from pathlib import Path

import pytest

from skypro.domain.enums import WorkType
from skypro.infra.repositories import get_works_prices
from skypro.infra.repositories.errors import PriceLoadError


@pytest.fixture
def mocked_base_dir(monkeypatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(f'{get_works_prices.__module__}.BASE_DIR', tmp_path)
    return tmp_path


@pytest.fixture
def work_prices_file(mocked_base_dir: Path) -> Path:
    return mocked_base_dir / 'work_prices.json'


@pytest.mark.parametrize('work_type', WorkType)
def test_read_all_supported_work_types(work_prices_file, work_type):
    data = {str(work_type): 100}
    work_prices_file.write_text(json.dumps(data))

    [result] = get_works_prices()

    assert result.work_type == work_type
    assert result.price == Decimal(100)


def test_file_not_found_error(work_prices_file):
    work_prices_file.unlink(missing_ok=True)
    with pytest.raises(PriceLoadError):
        get_works_prices()


def test_invalid_format_error(work_prices_file):
    work_prices_file.write_text('unsupported_format')
    with pytest.raises(PriceLoadError):
        get_works_prices()


def test_invalid_structure_error(work_prices_file):
    work_prices_file.write_text(json.dumps(['a', 'b', 'c']))
    with pytest.raises(PriceLoadError):
        get_works_prices()


def test_unknown_work_type_error(work_prices_file):
    data = {'unknown_work_type': 100}
    work_prices_file.write_text(json.dumps(data))

    with pytest.raises(PriceLoadError):
        get_works_prices()


@pytest.mark.parametrize(
    'invalid_price_format', ['', {}, []], ids=['string', 'dict', 'list']
)
def test_invalid_price_error(work_prices_file, work_type, invalid_price_format):
    data = {str(work_type): invalid_price_format}
    work_prices_file.write_text(json.dumps(data))

    with pytest.raises(PriceLoadError):
        get_works_prices()
