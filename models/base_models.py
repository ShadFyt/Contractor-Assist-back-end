from datetime import date
from sqlmodel import SQLModel, Field
from typing import Optional

from humps import camelize


def to_camel(string):
    return camelize(string)


class JobBase(SQLModel):
    job_name: Optional[str]
    is_complete: bool = False
    summary: Optional[str]
    start_date: Optional[date]
    finish_date: Optional[date]
    location: str
    job_type: Optional[str]

    client_id: Optional[int] = Field(default=None, foreign_key="client.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EmployeeBase(SQLModel):
    first_name: str
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

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class TaskBase(SQLModel):
    task: str
    is_complete: bool = False

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class ClientBase(SQLModel):
    first_name: str
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
