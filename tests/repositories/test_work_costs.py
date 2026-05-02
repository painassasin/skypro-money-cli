import json
from pathlib import Path

import pytest

from skypro.repositories.work_costs import load_work_costs


@pytest.fixture(autouse=True)
def clear_load_work_costs_cache():
    load_work_costs.cache_clear()
    yield
    load_work_costs.cache_clear()


@pytest.fixture
def mocked_base_dir(tmp_path, monkeypatch):
    monkeypatch.setattr('skypro.repositories.work_costs.BASE_DIR', tmp_path)
    return tmp_path


@pytest.fixture
def work_costs_file(mocked_base_dir):
    work_costs_file = mocked_base_dir / 'work_costs.json'
    work_costs_file.touch()
    return work_costs_file


def test_load_work_costs_returns_data_from_json_file(work_costs_file):
    expected = {'ДЗ': 100, 'КР': 200}
    work_costs_file.write_text(json.dumps(expected))

    result = load_work_costs()

    assert result == expected


@pytest.mark.usefixtures('mocked_base_dir')
def test_load_work_costs_raises_runtime_error_when_file_not_found():
    with pytest.raises(RuntimeError, match='Failed to load work costs') as e:
        load_work_costs()

    assert isinstance(e.value.__cause__, FileNotFoundError)


def test_load_work_costs_raises_runtime_error_for_invalid_json(work_costs_file):
    work_costs_file.write_text('{invalid json')

    with pytest.raises(RuntimeError, match='Failed to load work costs') as e:
        load_work_costs()

    assert isinstance(e.value.__cause__, json.JSONDecodeError)


def test_load_work_costs_uses_cached_value(work_costs_file, mocker):
    work_costs_file.write_text(json.dumps({'ДЗ': 100}))
    open_spy = mocker.spy(Path, 'open')

    [load_work_costs() for _ in range(10)]

    assert open_spy.call_count == 1
