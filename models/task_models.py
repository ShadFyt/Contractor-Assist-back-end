from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .jobs_models import Job


from humps import camelize


def to_camel(string):
    return camelize(string)


class TaskBase(SQLModel):
    task: str = Field(index=True)
    is_complete: bool = False

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    job: Optional["Job"] = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass

    class Config:
        schema_extra = {"example": {"task": "Some task", "is_complete": False}}


class TaskUpdate(TaskBase):
    pass


class TaskDelete(TaskBase):
    pass
