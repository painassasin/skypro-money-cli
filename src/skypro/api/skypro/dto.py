from pydantic import BaseModel, Field


class ServiceSummary(BaseModel, populate_by_name=True):
    homework: int = Field(0, alias='ДЗ', ge=0)
    coursework: int = Field(0, alias='КР', ge=0)
    diploma: int = Field(0, alias='ДР', ge=0)
    live: int = Field(0, alias='Лайв', ge=0)
    individual_consultation: int = Field(0, alias='ИК', ge=0)


class AccountDataResponse(BaseModel):
    services_summary: ServiceSummary
