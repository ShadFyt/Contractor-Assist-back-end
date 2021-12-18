from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .employee_models import Employee
    from .jobs_models import Job


class TimeEntriesBase(SQLModel):
    date: str
    clock_in: datetime
    clock_out: datetime
    hours: Optional[int]

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")


class TimeEntries(TimeEntriesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    employee: Optional["Employee"] = Relationship(back_populates="time_entries")
    job: Optional["Job"] = Relationship(back_populates="time_entries")


class TimeEntriesRead(TimeEntriesBase):
    id: int
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass
