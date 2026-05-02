from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class WorkType(StrEnum):
    HOMEWORK = 'Домашние работы'
    COURSEWORK = 'Курсовые работы'
    DIPLOMA = 'Дипломные работы'
    LIVE = 'Лайвы'
    CONSULTATION = 'Консультации'


@dataclass(frozen=True)
class WorkItem:
    type: WorkType
    count: int
    unit_price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.count
