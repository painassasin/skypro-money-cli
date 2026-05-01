import logging
from functools import cache
from logging.handlers import RotatingFileHandler

from .settings import BASE_DIR, settings

LOG_DIR = BASE_DIR / 'logs'


@cache
def configure_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=LOG_DIR / 'skypro.log', maxBytes=10_000, backupCount=5
    )

    logging.basicConfig(
        level=settings.log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[file_handler],
    )

    logging.getLogger('httpx').setLevel(logging.WARNING)
