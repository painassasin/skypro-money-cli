from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class WorkType(StrEnum):
    HOMEWORK = 'homework'
    COURSEWORK = 'coursework'
    DIPLOMA = 'diploma'
    LIVE = 'live'
    CONSULTATION = 'consultation'

    @property
    def label(self) -> str:
        return {
            WorkType.HOMEWORK: 'Домашние работы',
            WorkType.COURSEWORK: 'Курсовые работы',
            WorkType.DIPLOMA: 'Дипломные работы',
            WorkType.LIVE: 'Лайвы',
            WorkType.CONSULTATION: 'Консультации',
        }[self]


@dataclass(frozen=True)
class WorkItem:
    type: WorkType
    count: int
    unit_price: Decimal

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.count
