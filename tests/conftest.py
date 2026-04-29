from collections.abc import Iterator

import pytest
from aioresponses.core import aioresponses

from config import BASE_DIR


@pytest.fixture(autouse=True)
def mock_http() -> Iterator[aioresponses]:
    with aioresponses() as m:
        yield m


@pytest.fixture(scope='session')
def fixtures_dir():
    return BASE_DIR / 'tests' / 'fixtures'
