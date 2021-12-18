from typing import Optional
from sqlmodel import SQLModel

from .base_models import EmployeeBase
from .jobs_models import JobRead


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


class EmployeeReadWithJob(EmployeeRead):
    job: Optional[JobRead] = None
