from datetime import date

from pydantic import ValidationError

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkSummary
from skypro.infra.api.errors import ApiError, AuthenticationError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.http.client import HttpClient
from skypro.infra.http.errors import HttpError
from skypro.infra.repositories.errors import SummaryLoadError


async def get_summary(start_date: date, end_date: date) -> list[WorkSummary]:
    try:
        async with HttpClient() as http_client:
            skypro = SkyProClient(http_client)
            account_data = await skypro.get_account_data(start_date, end_date)
    except AuthenticationError as e:
        message = 'SkyPro authentication failed. Check email and password.'
        raise SummaryLoadError(message) from e
    except (HttpError, ApiError, ValidationError) as e:
        raise SummaryLoadError(str(e) or 'Failed to load summary from SkyPro.') from e

    return [
        WorkSummary(WorkType.HOMEWORK, account_data.services_summary.homework),
        WorkSummary(WorkType.COURSEWORK, account_data.services_summary.coursework),
        WorkSummary(WorkType.DIPLOMA, account_data.services_summary.diploma),
        WorkSummary(WorkType.LIVE, account_data.services_summary.live),
        WorkSummary(
            WorkType.CONSULTATION, account_data.services_summary.individual_consultation
        ),
    ]
