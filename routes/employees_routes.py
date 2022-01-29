from fastapi import APIRouter, status, Depends
from typing import List

from sqlmodel import Session
from services import employees_utils

from models.employee_models import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeUpdate,
)
from models.db import get_session


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeRead])
async def show_all_employees(session: Session = Depends(get_session)):
    return employees_utils.get_all(session)


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee_by_id(
    *, session: Session = Depends(get_session), employee_id: int
):
    return employees_utils.get_one_by_id(session, employee_id)


@router.get("/name/{employee_name}", response_model=EmployeeRead)
async def get_employee_by_name(
    *, session: Session = Depends(get_session), employee_name: str
):
    return employees_utils.get_one_by_name(session, employee_name)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeRead)
def create_employee(
    *, session: Session = Depends(get_session), employee: EmployeeCreate
):
    return employees_utils.create(session, employee)


@router.patch(
    "/{employee_id}", status_code=status.HTTP_202_ACCEPTED, response_model=EmployeeRead
)
def update_employee(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    employee: EmployeeUpdate
):
    return employees_utils.modify(session, employee_id, employee)


@router.delete("/{employee_id}")
def delete_employee(*, session: Session = Depends(get_session), employee_id: int):
    employees_utils.destroy(session, employee_id)
    return {status.HTTP_204_NO_CONTENT: True}
