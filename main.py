import asyncio
import logging

from clients.http_client import HttpClient
from config import settings

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main() -> None:
    client = HttpClient(base_url=settings.skypro.base_url, timeout=3)

    async with client as api_client:
        response = await api_client.options(settings.skypro.login_url)
        logger.info(response)
        response.release()


if __name__ == '__main__':
    asyncio.run(main())
