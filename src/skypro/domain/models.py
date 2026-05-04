from dataclasses import dataclass
from decimal import Decimal

from .enums import WorkType
from .errors import InvalidPriceError


@dataclass(slots=True, frozen=True)
class WorkPrice:
    work_type: WorkType
    price: Decimal

    def __post_init__(self) -> None:
        if self.price <= Decimal(0):
            raise InvalidPriceError
