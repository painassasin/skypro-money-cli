from collections.abc import Iterator
from pathlib import Path

import pytest
from aioresponses.core import aioresponses


@pytest.fixture(autouse=True)
def mock_http() -> Iterator[aioresponses]:
    with aioresponses() as m:
        yield m


@pytest.fixture(scope='session')
def fixtures_dir():
    return Path(__file__).parent.resolve() / 'fixtures'
