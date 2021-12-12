from sqlmodel import SQLModel, Field
from typing import Optional


class EmployeeBase(SQLModel):
    first_name: str
    last_name: str
    birth_day: int
    pay_rate: float


class Employee(EmployeeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int


class EmployeeUpdate(EmployeeBase):
    pass
