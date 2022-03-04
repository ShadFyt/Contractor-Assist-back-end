from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel
from datetime import date


from humps import camelize


if TYPE_CHECKING:
    from employee_models import EmployeeRead, EmployeeReadName, Employee
    from jobs_models import Job


def to_camel(string):
    return camelize(string)


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


class TimeEntries(TimeEntriesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    employee: Optional["Employee"] = Relationship(back_populates="time_entries")
    job: Optional["Job"] = Relationship(back_populates="time_entries")


class TimeEntriesRead(TimeEntriesBase):
    id: int
    # employee: Optional["EmployeeRead"] = None


class TimeEntriesReadEmployee(TimeEntriesRead):
    employee: Optional["EmployeeRead"] = None


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass
