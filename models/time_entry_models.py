from typing import TYPE_CHECKING, Optional

from humps import camelize

from .base_models import TimeEntriesBase


if TYPE_CHECKING:
    from employee_models import EmployeeRead, EmployeeReadName


def to_camel(string):
    return camelize(string)


class TimeEntriesRead(TimeEntriesBase):
    id: int
    # employee: Optional["EmployeeRead"] = None


class TimeEntriesReadEmployee(TimeEntriesRead):
    employee: Optional["EmployeeRead"] = None


class TimeEntriesCreate(TimeEntriesBase):
    pass


class TimeEntriesUpdate(TimeEntriesBase):
    pass


class TimeEntriesDelete(TimeEntriesBase):
    pass
