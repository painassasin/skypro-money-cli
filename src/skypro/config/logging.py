import logging

from .settings import settings

logging.basicConfig(
    level=settings.log_level, format='%(asctime)s - %(levelname)s - %(message)s'
)


def configure_logging() -> None:
    logging.getLogger('httpx').setLevel(logging.WARNING)
