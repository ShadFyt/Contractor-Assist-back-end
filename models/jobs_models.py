from typing import List

from models.task_models import TaskRead
from .base_models import JobBase
from .time_entry_models import TimeEntriesRead
from humps import camelize


def to_camel(string):
    return camelize(string)


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
