import asyncio
import logging
from datetime import UTC, date, datetime

from clients import SkyProClient

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main() -> None:
    now = datetime.now(UTC)

    async with SkyProClient() as client:
        await client.login()
        account_data = await client.get_account_data(
            start_date=date(now.year, now.month, 1),
            end_date=date(now.year, now.month, now.day),
        )
        logging.info(account_data)  # noqa: LOG015


if __name__ == '__main__':
    asyncio.run(main())
