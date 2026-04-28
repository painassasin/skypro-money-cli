import asyncio
import logging

from clients import SkyProClient

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main() -> None:
    async with SkyProClient() as client:
        await client.login()


if __name__ == '__main__':
    asyncio.run(main())
