from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel

from .base_models import EmployeeBase

from .time_entry_models import TimeEntriesRead

if TYPE_CHECKING:
    from .time_entry_models import TimeEntriesRead


class EmployeeCreate(EmployeeBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "birth_date": "10/11/1995",
                "pay_rate": 20,
                "phone_number": 8889999999,
                "email": "fake@hotmail.com",
            }
        }


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeReadName(SQLModel):
    first_name: str


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeReadWithTimes(EmployeeRead):
    time_entries: Optional[TimeEntriesRead] = None
