from decimal import Decimal

from rich.table import Column, Table

from skypro.domain.enums import WorkType
from skypro.domain.models import WorkReportItem
from skypro.utils import format_price

work_type_translate_map = {
    WorkType.HOMEWORK: 'Домашние работы',
    WorkType.CONSULTATION: 'Индивидуальные консультации',
    WorkType.LIVE: 'Групповые занятия',
    WorkType.DIPLOMA: 'Дипломные работы',
    WorkType.COURSEWORK: 'Курсовые работы',
}


def render_summary_table(
    report: list[WorkReportItem],
    total: Decimal,
    total_after_tax: Decimal,
) -> Table:
    table = Table(
        Column('Тип', style='cyan'),
        Column('Количество', style='magenta', justify='center'),
        Column('Оплата', style='magenta', justify='right'),
        title='Статистика работ за месяц',
    )

    for item in report:
        if not item.quantity:
            continue

        table.add_row(
            work_type_translate_map[item.work_type],
            str(item.quantity),
            format_price(item.price),
        )

    table.add_section()
    table.add_row('Итого', '', format_price(total))
    table.add_row('После уплаты налога', '', format_price(total_after_tax))

    return table
