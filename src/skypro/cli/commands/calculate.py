from typer import Option


def calculate_command(
    year: int | None = Option(None, help='Year to calculate'),
    month: int | None = Option(None, help='Month to calculate'),
) -> None:
    """Calculate work costs."""
    print(f'Calculate command for {year}/{month}')  # noqa: T201
