# from sqlmodel import Field, Relationship
# from typing import List, Optional

# from .base_models import JobBase, EmployeeBase, TimeEntriesBase


# class Job(JobBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     time_entries: List["TimeEntries"] = Relationship(back_populates="job")


# class Employee(EmployeeBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     time_entries: List["TimeEntries"] = Relationship(back_populates="employee")


# class TimeEntries(TimeEntriesBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")

#     employee: Optional[Employee] = Relationship(back_populates="time_entries")
#     job: Optional["Job"] = Relationship(back_populates="time_entries")
