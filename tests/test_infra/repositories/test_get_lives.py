from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from skypro.config import settings
from skypro.domain.models import Live
from skypro.infra.api.errors import ApiError, AuthenticationError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.api.skypro.dto import AccountDataResponse
from skypro.infra.http.errors import HttpError
from skypro.infra.repositories.errors import LivesLoadError
from skypro.infra.repositories.get_lives import get_lives


@pytest.fixture
def account_data_response(account_data) -> AccountDataResponse:
    tz = ZoneInfo(settings.get_settings().skypro.tz)
    account_data['lives'] = [
        {'title': 'Late live', 'date': datetime(2026, 1, 3, 19, 0, tzinfo=tz)},
        {'title': 'Early live', 'date': datetime(2026, 1, 1, 18, 0, tzinfo=tz)},
    ]
    return AccountDataResponse.model_validate(account_data)


@pytest.fixture
def mocked_get_account_data(mocker, account_data_response):
    return mocker.patch.object(
        SkyProClient, 'get_account_data', return_value=account_data_response
    )


@pytest.mark.usefixtures('mocked_get_account_data')
async def test_get_lives_returns_sorted_lives():
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)
    tz = ZoneInfo(settings.get_settings().skypro.tz)

    lives = await get_lives(start_date, end_date)

    assert lives == [
        Live('Early live', datetime(2026, 1, 1, 18, 0, tzinfo=tz)),
        Live('Late live', datetime(2026, 1, 3, 19, 0, tzinfo=tz)),
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
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)

    with pytest.raises(LivesLoadError):
        await get_lives(start_date, end_date)


async def test_authentication_error_has_readable_message(mocked_get_account_data):
    mocked_get_account_data.side_effect = AuthenticationError('Authentication failed')
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)

    with pytest.raises(
        LivesLoadError,
        match=r'SkyPro authentication failed\. Check email and password\.',
    ):
        await get_lives(start_date, end_date)


async def test_http_error_message_is_preserved(mocked_get_account_data):
    mocked_get_account_data.side_effect = HttpError('Network error: GET test-url')
    start_date, end_date = date(2026, 1, 1), date(2026, 1, 31)

    with pytest.raises(LivesLoadError, match='Network error: GET test-url'):
        await get_lives(start_date, end_date)
