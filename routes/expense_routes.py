from fastapi import APIRouter, status, Depends
from typing import List

from sqlmodel import Session
from internal import admin

from models.expense_model import (
    ExpenseCreate,
    ExpenseDelete,
    ExpenseRead,
    ExpenseUpdate,
    Expense,
)

from models.db import get_session


router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
    dependencies=[Depends(admin.get_current_active_user)],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_expense():
    return {"CREATED": True}


@router.get("/", status_code=status.HTTP_200_OK)
def read_all():
    return {"READ": "grabbing all items from db"}


@router.patch("/{expense_id}")
def update_expense_by_id(*, expense_id: int):
    return {"UPDATE": f"updated {expense_id}"}


@router.delete("/{expense_id}")
def delete_expense_by_id(expense_id: int):
    return {"DELETE": f"deleting {expense_id}"}
