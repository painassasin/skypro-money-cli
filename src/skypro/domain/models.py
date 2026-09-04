from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from .enums import WorkType
from .errors import InvalidPriceError, InvalidQuantityError


@dataclass(slots=True, frozen=True)
class WorkPrice:
    work_type: WorkType
    price: Decimal

    def __post_init__(self) -> None:
        if self.price <= Decimal(0):
            raise InvalidPriceError


@dataclass(slots=True, frozen=True)
class WorkSummary:
    work_type: WorkType
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise InvalidQuantityError


@dataclass(frozen=True)
class WorkReportItem:
    work_type: WorkType
    quantity: int
    price: Decimal
    total: Decimal


@dataclass(frozen=True)
class Live:
    title: str
    date: datetime
