import locale

from skypro.cli.app import app
from skypro.config import configure_logging


def main() -> None:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    configure_logging()
    app()


if __name__ == '__main__':
    main()
