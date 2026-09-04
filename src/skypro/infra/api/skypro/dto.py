from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

from skypro.config import settings


class ServiceSummary(BaseModel, populate_by_name=True):
    homework: int = Field(0, alias='ДЗ', ge=0)
    coursework: int = Field(0, alias='КР', ge=0)
    diploma: int = Field(0, alias='ДР', ge=0)
    live: int = Field(0, alias='Лайв', ge=0)
    individual_consultation: int = Field(0, alias='ИК', ge=0)


class ServiceByProfession(BaseModel):
    profession: str
    services: ServiceSummary


class LiveInfo(BaseModel, strict=True):
    title: str
    date: datetime

    @field_validator('date', mode='before')
    @classmethod
    def parse_datetime(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value

        dt = datetime.strptime(value, '%d %B %Y %H:%M')  # ruff:ignore[call-datetime-strptime-without-zone]
        return dt.replace(tzinfo=ZoneInfo(settings.get_settings().skypro.tz))


class AccountDataResponse(BaseModel):
    services_by_profession: list[ServiceByProfession]
    lives: list[LiveInfo]
