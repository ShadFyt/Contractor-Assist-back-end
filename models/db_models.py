from sqlmodel import Field, Relationship
from typing import List, Optional

from .base_models import ClientBase, JobBase, EmployeeBase, TimeEntriesBase, TaskBase


class Job(JobBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="job")
    tasks: List["Task"] = Relationship(back_populates="job")
    client: Optional["Client"] = Relationship(back_populates="jobs")


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="employee")


class TimeEntries(TimeEntriesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    employee: Optional[Employee] = Relationship(back_populates="time_entries")
    job: Optional[Job] = Relationship(back_populates="time_entries")


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    job: Optional[Job] = Relationship(back_populates="tasks")


class Client(ClientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jobs: List[Job] = Relationship(back_populates="client")
