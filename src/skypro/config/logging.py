import logging
import logging.config
from functools import cache
from typing import Any

from rich.console import Console
from rich.logging import RichHandler

from .settings import HOME_DIR, get_settings

LOG_DIR = HOME_DIR / 'logs'

LOGGING_CONFIG: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'formatter': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'skypro.log',
            'maxBytes': 10 * 1024,  # 10Mb
            'backupCount': 5,
            'formatter': 'formatter',
        },
    },
    'root': {'handlers': ['file']},
    'loggers': {
        'httpx': {'handlers': ['file'], 'level': logging.WARNING, 'propagate': True},
    },
}


@cache
def configure_logging() -> None:
    LOG_DIR.mkdir(mode=0o700, exist_ok=True, parents=True)
    LOGGING_CONFIG['root']['level'] = get_settings().log_level.upper()
    logging.config.dictConfig(LOGGING_CONFIG)


def enable_console_logging(console: Console) -> None:
    root_logger = logging.getLogger()
    console_handler = RichHandler(
        console=console, rich_tracebacks=True, show_time=False
    )
    root_logger.addHandler(console_handler)
