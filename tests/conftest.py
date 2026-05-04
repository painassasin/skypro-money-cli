import random

import pytest

from skypro.domain.enums import WorkType


@pytest.fixture
def work_type() -> WorkType:
    return random.choice(list(WorkType))
