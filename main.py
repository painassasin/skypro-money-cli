import asyncio
import logging

from use_cases import get_work_summary

logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main() -> None:
    work_summary = await get_work_summary(2026, 4)
    for item in work_summary:
        logger.info(item)


if __name__ == '__main__':
    asyncio.run(main())
