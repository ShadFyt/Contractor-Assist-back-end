from fastapi import APIRouter, status, Depends
from typing import List

from sqlmodel import Session
from services.dal import EmployeeDal
from internal import admin

from models.employee_models import (
    EmployeeCreate,
    EmployeeRead,
    EmployeeReadWithTimes,
    EmployeeUpdate,
)
from models.db import get_session
from models.employee_models import Employee


router = APIRouter(prefix="/employees", tags=["employees"])

employee_dal = EmployeeDal()


@router.get(
    "/",
    response_model=List[EmployeeRead],
    dependencies=[Depends(admin.get_current_active_user)],
    status_code=200,
)
async def show_all_employees(session: Session = Depends(get_session)):
    return employee_dal.get_all(session)


@router.get("/{employee_id}", response_model=EmployeeRead)
async def get_employee_by_id(
    *, session: Session = Depends(get_session), employee_id: int
):

    employee: Employee = employee_dal.get_one_by_id(session, employee_id)
    print("employee time sheet :", employee.time_entries[0])
    return employee


@router.get("/name/{employee_name}", response_model=EmployeeRead)
async def get_employee_by_name(
    *, session: Session = Depends(get_session), employee_name: str
):
    return employee_dal.get_one_by_name(session, employee_name)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeRead)
def create_employee(
    *, session: Session = Depends(get_session), employee: EmployeeCreate
):
    return employee_dal.create(session, employee)


@router.patch(
    "/{employee_id}", status_code=status.HTTP_202_ACCEPTED, response_model=EmployeeRead
)
def update_employee(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    employee: EmployeeUpdate
):
    return employee_dal.modify(session, employee_id, employee)


@router.delete("/{employee_id}")
def delete_employee(*, session: Session = Depends(get_session), employee_id: int):
    employee_dal.destroy(session, employee_id)
    return {status.HTTP_204_NO_CONTENT: True}
