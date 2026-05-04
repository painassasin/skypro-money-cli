from datetime import date

import pytest

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkSummary
from skypro.infra.api.errors import ApiError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.api.skypro.dto import AccountDataResponse
from skypro.infra.http.errors import HttpError
from skypro.infra.repositories.errors import SummaryLoadError
from skypro.infra.repositories.summary import get_summary


@pytest.fixture
def account_data() -> dict:
    return {
        'services_summary': {
            'ДЗ': 1,
            'КР': 2,
            'ДР': 3,
            'Лайв': 4,
            'ИК': 5,
        }
    }


@pytest.fixture
def account_data_response(account_data) -> AccountDataResponse:
    return AccountDataResponse.model_validate(account_data)


@pytest.fixture
def mocked_get_account_data(mocker, account_data_response):
    return mocker.patch.object(
        SkyProClient, 'get_account_data', return_value=account_data_response
    )


@pytest.mark.usefixtures('mocked_get_account_data')
async def test_get_summary_info():
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 2)

    summary = await get_summary(start_date, end_date)

    assert summary == [
        WorkSummary(WorkType.HOMEWORK, 1),
        WorkSummary(WorkType.COURSEWORK, 2),
        WorkSummary(WorkType.DIPLOMA, 3),
        WorkSummary(WorkType.LIVE, 4),
        WorkSummary(WorkType.CONSULTATION, 5),
    ]


@pytest.mark.parametrize(
    'handled_error',
    [HttpError, ApiError, lambda *_: AccountDataResponse.model_validate({})],
    ids=['http error', 'api error', 'validation_error'],
)
async def test_invalid_sky_pro_api_response_raises_error(
    mocked_get_account_data, handled_error
):
    mocked_get_account_data.side_effect = handled_error
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 2)

    with pytest.raises(SummaryLoadError):
        await get_summary(start_date, end_date)
