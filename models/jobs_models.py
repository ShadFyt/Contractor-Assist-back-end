from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING


if TYPE_CHECKING:
    from .time_entry_models import TimeEntries, TimeEntriesRead


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


class JobReadWithTimes(JobRead):
    time_entries: List["TimeEntriesRead"] = []
