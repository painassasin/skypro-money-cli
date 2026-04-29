from pathlib import Path

import pytest

from utils.work_costs import get_work_costs


@pytest.fixture(autouse=True)
def clear_get_work_costs_cache():
    get_work_costs.cache_clear()
    yield
    get_work_costs.cache_clear()


@pytest.fixture
def mocked_base_dir(tmp_path, monkeypatch) -> Path:
    monkeypatch.setattr('utils.work_costs.BASE_DIR', tmp_path)
    return tmp_path


def test_get_work_costs_reads_work_costs_from_json(mocked_base_dir):
    file_path = mocked_base_dir / 'work_costs.json'
    file_path.write_text('{"ДЗ": 10, "КР": 5, "ДР": 6, "Лайв": 3, "ИК": 4}')

    result = get_work_costs()

    assert result == {
        'ДЗ': 10,
        'КР': 5,
        'ДР': 6,
        'Лайв': 3,
        'ИК': 4,
    }
