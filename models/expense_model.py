from .base_models import ExpenseBase


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
