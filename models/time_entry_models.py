from sqlmodel import Field
from typing import TYPE_CHECKING, Optional

from humps import camelize

from .base_models import TimeEntriesBase


if TYPE_CHECKING:
    from models.employee_models import EmployeeRead


def to_camel(string):
    return camelize(string)

class TimeEntriesRead(TimeEntriesBase):
    id: int
    employee_id: Optional[int] = Field(default=None, foreign_key="employee.id")


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass
