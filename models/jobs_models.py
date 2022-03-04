from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date


from models.task_models import TaskRead
from .time_entry_models import TimeEntriesRead
from humps import camelize

if TYPE_CHECKING:
    from .db_models import TimeEntries, Task, Client, Expense


def to_camel(string):
    return camelize(string)


class JobBase(SQLModel):
    job_name: str = Field(index=True)
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


class Job(JobBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="job")
    tasks: List["Task"] = Relationship(back_populates="job")
    client: Optional["Client"] = Relationship(back_populates="jobs")
    expenses: List["Expense"] = Relationship(back_populates="job")


class JobRead(JobBase):
    id: int

    # class Config:
    #     alias_generator = to_camel


class JobCreate(JobBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "job_name": "Lake view house",
                "is_complete": False,
                "start_date": "10/10/2021",
                "finish_date": "17/10/2021",
                "location": "24 lake Dr",
                "job_type": "Sanding",
                "client_id": 1,
            }
        }


class JobUpdate(JobBase):
    pass


class JobReadWithTimes(JobRead):
    time_entries: List[TimeEntriesRead] = []


class JobReadWithTasks(JobRead):
    tasks: List[TaskRead] = []


class JobReadWithTasksAndTimes(JobRead):
    tasks: List[TaskRead] = []
    time_entries: List[TimeEntriesRead] = []
