from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date


from humps import camelize


if TYPE_CHECKING:
    from .jobs_models import Job


def to_camel(string):
    return camelize(string)


class ExpenseBase(SQLModel):
    store: str
    price: float
    location: Optional[str]
    date: date
    tax: Optional[float]

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Expense(ExpenseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job: Optional["Job"] = Relationship(back_populates="expenses")


class ExpenseRead(ExpenseBase):
    id: int


class ExpenseCreate(ExpenseBase):
    pass

    class Config:
        schema_extra = ...


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseDelete(ExpenseBase):
    pass
