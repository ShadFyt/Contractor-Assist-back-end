from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional

from humps import camelize


def to_camel(string):
    return camelize(string)


class EmployeeBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str
    email: str
    phone_number: int
    birth_date: date
    pay_rate: float

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TimeEntriesBase(SQLModel):
    date: date
    clock_in: str
    clock_out: str
    hours: Optional[int]

    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TaskBase(SQLModel):
    task: str = Field(index=True)
    is_complete: bool = False

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ClientBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str
    phone_number: str
    email: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ExpenseBase(SQLModel):
    store: str
    price: float
    location: Optional[str]
    date: date
    tax: Optional[float]

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
