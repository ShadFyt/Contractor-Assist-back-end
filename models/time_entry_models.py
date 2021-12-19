from sqlmodel import Field
from typing import Optional

from .base_models import TimeEntriesBase


class TimeEntriesRead(TimeEntriesBase):
    id: int
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass
