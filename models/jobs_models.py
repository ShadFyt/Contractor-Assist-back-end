from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class JobBase(SQLModel):
    job_name: Optional[str]
    is_complete: bool = False
    summary: Optional[str]
    start_date: Optional[str]
    finish_date: Optional[str]
    job_type: Optional[str]


class Job(JobBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="job")


class JobRead(JobBase):
    id: int


class JobCreate(JobBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "job_name": "Lake view house",
                "is_complete": False,
                "start_date": "10/10/2021",
                "finish_date": "17/10/2021",
                "job_type": "Sanding",
            }
        }


class JobUpdate(JobBase):
    pass


class EmployeeBase(SQLModel):
    first_name: str
    last_name: str
    birth_date: str
    pay_rate: float


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="employee")


class EmployeeCreate(EmployeeBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "10/11/1995",
                "pay_rate": 20,
            }
        }


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeReadName(SQLModel):
    first_name: str


class EmployeeUpdate(EmployeeBase):
    pass


class TimeEntriesBase(SQLModel):
    date: str
    clock_in: datetime
    clock_out: datetime
    hours: Optional[int]

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")


class TimeEntries(TimeEntriesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    employee: Optional[Employee] = Relationship(back_populates="time_entries")
    job: Optional["Job"] = Relationship(back_populates="time_entries")


class TimeEntriesRead(TimeEntriesBase):
    id: int


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass


class EmployeeReadWithJob(EmployeeRead):
    job: Optional[JobRead] = None


class JobReadWithTimes(JobRead):
    time_entries: List[TimeEntriesRead] = []
