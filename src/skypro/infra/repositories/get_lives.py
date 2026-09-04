from datetime import date

from pydantic import ValidationError

from skypro.domain.models import Live
from skypro.infra.api.errors import ApiError, AuthenticationError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.http.client import HttpClient
from skypro.infra.http.errors import HttpError

from .errors import LivesLoadError


async def get_lives(start_date: date, end_date: date) -> list[Live]:
    try:
        async with HttpClient() as http_client:
            skypro = SkyProClient(http_client)
            account_data = await skypro.get_account_data(start_date, end_date)
    except AuthenticationError as e:
        message = 'SkyPro authentication failed. Check email and password.'
        raise LivesLoadError(message) from e
    except (HttpError, ApiError, ValidationError) as e:
        raise LivesLoadError(str(e) or 'Failed to load lives from SkyPro.') from e

    return [
        Live(title=live.title, date=live.date)
        for live in sorted(account_data.lives, key=lambda x: x.date)
    ]
