from sqlmodel import SQLModel, Field
from typing import Optional

from sqlmodel.main import Relationship
from .jobs_models import Job, JobRead


class EmployeeBase(SQLModel):
    first_name: str
    last_name: str
    birth_day: int
    pay_rate: float

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    job: Optional[Job] = Relationship(back_populates="employees")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeReadWithJob(EmployeeRead):
    job: Optional[JobRead] = None
