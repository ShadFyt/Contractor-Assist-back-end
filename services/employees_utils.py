from fastapi import status, HTTPException

from sqlmodel import Session, select
from models import employee_models
from models import db_models


def get_all(session: Session):
    print("getting employyes")
    return session.exec(select(db_models.Employee)).all()


def get_one_by_id(session: Session, employee_id: int):
    return session.get(db_models.Employee, employee_id)


def get_one_by_name(session: Session, employee_name: str):
    return session.exec(
        select(db_models.Employee).where(db_models.Employee.first_name == employee_name)
    ).one_or_none()


def create(session: Session, employee: employee_models.EmployeeCreate):
    db_employee = db_models.Employee.from_orm(employee)
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def modify(
    session: Session, employee_id: int, employee: employee_models.EmployeeUpdate
):
    db_employee = session.get(db_models.Employee, employee_id)
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


def destroy(session: Session, employee_id: int):
    employee = session.get(db_models.Employee, employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found"
        )

    session.delete(employee)
    session.commit()
