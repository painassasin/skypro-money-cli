import asyncio
from datetime import date

from skypro.api.http.client import HttpClient
from skypro.api.skypro.client import SkyProClient
from skypro.config.logging import configure_logging

configure_logging()


async def my_app() -> None:
    async with HttpClient() as http_client:
        skypro = SkyProClient(http_client)
        result = await skypro.get_account_data(
            start_date=date(2026, 4, 1),
            end_date=date(2026, 4, 30),
        )

        print(result)  # noqa: T201


def main() -> None:
    asyncio.run(my_app())


if __name__ == '__main__':
    main()
