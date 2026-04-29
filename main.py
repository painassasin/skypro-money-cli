import asyncio
import logging
from datetime import UTC, date, datetime

from clients.skypro_client import SkyProClient

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main() -> None:
    now = datetime.now(UTC)

    async with SkyProClient() as client:
        data = await client.get_account_data(
            start_date=date(now.year, now.month, 1),
            end_date=date(now.year, now.month, now.day),
        )
    logger.info(data)


if __name__ == '__main__':
    asyncio.run(main())
