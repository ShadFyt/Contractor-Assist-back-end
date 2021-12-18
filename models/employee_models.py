from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Relationship, Field

# from .jobs_models import JobRead


if TYPE_CHECKING:
    from .time_entry_models import TimeEntries


class EmployeeBase(SQLModel):
    first_name: str
    last_name: str
    birth_date: str
    pay_rate: float


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
            }
        }


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeReadName(SQLModel):
    first_name: str


class EmployeeUpdate(EmployeeBase):
    pass


# class EmployeeReadWithJob(EmployeeRead):
#     job: Optional[JobRead] = None
