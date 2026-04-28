from collections.abc import Iterator

import pytest
from aioresponses.core import aioresponses


@pytest.fixture(autouse=True)
def mock_aioresponse() -> Iterator[aioresponses]:
    with aioresponses() as m:
        yield m
