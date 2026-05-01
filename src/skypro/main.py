import locale

from skypro.cli import app
from skypro.config.logging import configure_logging

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

configure_logging()


def main() -> None:
    app()


if __name__ == '__main__':
    main()
