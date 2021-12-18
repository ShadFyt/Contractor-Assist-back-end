from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from sqlmodel import Session, select

from models.jobs_models import (
    Employee,
    EmployeeCreate,
    EmployeeRead,
    EmployeeReadWithJob,
    EmployeeUpdate,
)
from models.db import get_session


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeRead])
async def show_all_employees(session: Session = Depends(get_session)):
    return session.exec(select(Employee)).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeRead)
def create_employee(
    *, session: Session = Depends(get_session), employee: EmployeeCreate
):
    db_employee = Employee.from_orm(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.patch(
    "/{employee_id}", status_code=status.HTTP_202_ACCEPTED, response_model=EmployeeRead
)
def update_employee(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    employee: EmployeeUpdate
):
    db_employee = session.get(Employee, employee_id)
    if not db_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="employee not found"
        )
    employee_data = employee.dict(exclude_unset=True)
    for k, v in employee_data.items():
        setattr(db_employee, k, v)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


@router.delete("/{employee_id}")
def delete_employee(*, session: Session = Depends(get_session), employee_id: int):

    employee = session.get(Employee, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    session.delete(employee)
    session.commit()
    return {status.HTTP_204_NO_CONTENT: True}
