import locale

from skypro.config.logging import configure_logging

from .app import app


def main() -> None:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    configure_logging()
    app()


if __name__ == '__main__':
    main()
