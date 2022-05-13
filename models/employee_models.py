from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Relationship, Field
from humps import camelize
from datetime import date


from .time_entry_models import TimeEntriesRead

if TYPE_CHECKING:
    from .time_entry_models import TimeEntriesRead
    from db_models import TimeEntries


def to_camel(string):
    return camelize(string)


# sourcery skip: avoid-builtin-shadow
class EmployeeBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    pay_rate: float

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time_entries: List["TimeEntries"] = Relationship(back_populates="employee")


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
