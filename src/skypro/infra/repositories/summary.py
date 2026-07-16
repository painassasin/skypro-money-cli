import logging
from collections import defaultdict
from datetime import date
from itertools import starmap

from pydantic import ValidationError

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkSummary
from skypro.infra.api.errors import ApiError, AuthenticationError
from skypro.infra.api.skypro.client import SkyProClient
from skypro.infra.api.skypro.dto import ServiceByProfession, ServiceSummary
from skypro.infra.http.client import HttpClient
from skypro.infra.http.errors import HttpError
from skypro.infra.repositories.errors import SummaryLoadError

logger = logging.getLogger(__name__)


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

    return _get_summary_by_service_by_profession(*account_data.services_by_profession)


def _get_summary_by_service_by_profession(
    *services_by_profession: ServiceByProfession,
) -> list[WorkSummary]:
    work_summary: dict[WorkType, int] = defaultdict(int)

    for sbp in services_by_profession:
        logger.debug('Calculate work summary by %r', sbp.profession)
        for summary in _get_summary_by_service_summary(sbp.services):
            work_summary[summary.work_type] += summary.quantity
    return list(starmap(WorkSummary, work_summary.items()))


def _get_summary_by_service_summary(
    service_summary: ServiceSummary,
) -> list[WorkSummary]:
    return [
        WorkSummary(WorkType.HOMEWORK, service_summary.homework),
        WorkSummary(WorkType.COURSEWORK, service_summary.coursework),
        WorkSummary(WorkType.DIPLOMA, service_summary.diploma),
        WorkSummary(WorkType.LIVE, service_summary.live),
        WorkSummary(WorkType.CONSULTATION, service_summary.individual_consultation),
    ]
