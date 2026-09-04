from rich.table import Column, Table

from skypro.domain.models import Live
from skypro.utils import get_local_timezone


def render_lives_table(*lives: Live) -> Table:
    local_tz = get_local_timezone()

    table = Table(
        Column('Название', style='cyan', justify='left'),
        Column(f'Время\n({local_tz})', style='magenta', justify='center'),
        title='Ближайшие лайвы',
    )

    date_format = '[bold cyan]%d.%m.%Y[/] [bold green]%H:%M[/]'
    for live in lives:
        table.add_row(live.title, live.date.astimezone(local_tz).strftime(date_format))

    return table
