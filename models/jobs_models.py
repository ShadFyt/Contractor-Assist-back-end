from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class JobBase(SQLModel):
    job_name: Optional[str]
    is_complete: bool = False
    summary: Optional[str]
    start_date: Optional[str]
    start_end: Optional[str]
    job_type: Optional[str]


class Job(JobBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    employees: List["Employee"] = Relationship(back_populates="job")


class JobRead(JobBase):
    id: int


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


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


class JobReadWithEmployees(JobRead):
    employees: List[EmployeeRead] = []
