import pytest


@pytest.fixture
def account_data() -> dict:
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
        ]
    }
