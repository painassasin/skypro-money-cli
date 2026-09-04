from skypro.domain.models import Live
from skypro.infra.repositories import get_lives
from skypro.utils import get_month_range


async def get_lives_info(year: int, month: int) -> list[Live]:
    start_date, end_date = get_month_range(year, month)
    return await get_lives(start_date, end_date)
