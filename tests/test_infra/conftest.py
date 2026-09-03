from typing import Any

import pytest


@pytest.fixture
def account_data() -> dict[str, Any]:
    return {
        'services_by_profession': [
            {
                'profession': 'Python-developer',
                'services': {
                    'ДЗ': 1,
                    'КР': 2,
                    'ДР': 3,
                    'Лайв': 4,
                    'ИК': 5,
                },
            }
        ],
        'lives': [],
    }
