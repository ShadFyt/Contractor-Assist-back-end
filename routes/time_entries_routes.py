from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from sqlmodel import Session, select

from models.time_entry_models import (
    TimeEntriesRead,
    TimeEntriesCreate,
    TimeEntriesDelete,
    TimeEntriesUpdate,
)
from models.db_models import Employee, TimeEntries

from models.db import get_session

router = APIRouter(tags=["Time Sheet"])


@router.get("/employee/{employee_id}/time_sheet", response_model=List[TimeEntriesRead])
def show_time_entries_by_employee(
    *, session: Session = Depends(get_session), employee_id: int
):
    employee = session.get(Employee, employee_id)
    print(employee.time_entries)
    return employee.time_entries


@router.post(
    "/employee/{employee_id}/time_sheet",
    response_model=TimeEntriesRead,
    status_code=status.HTTP_201_CREATED,
)
def time_entry_create(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    time_entry: TimeEntriesCreate
):
    db_time_entry = TimeEntries.from_orm(time_entry)
    employee = session.get(Employee, employee_id)
    employee.time_entries.append(db_time_entry)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return db_time_entry
