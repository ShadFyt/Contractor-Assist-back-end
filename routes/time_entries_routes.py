from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from sqlmodel import Session, select
from models import db_models

from models.time_entry_models import (
    TimeEntriesRead,
    TimeEntriesCreate,
    TimeEntriesDelete,
    TimeEntriesUpdate,
)
from models.db_models import Employee, Job, TimeEntries

from models.db import get_session
from services import dal

router = APIRouter(prefix="/time_sheet", tags=["Time Sheet"])

time_entry_dal = dal.TimeEntry(TimeEntries, "time entry")


@router.get("/{id}", response_model=TimeEntriesRead)
def get_time_entry_by_id(*, session: Session = Depends(get_session), id: int):
    return time_entry_dal.get_one_by_id(session, id)


@router.get("/employee/{employee_id}", response_model=List[TimeEntriesRead])
def show_time_entries_by_employee(
    *, session: Session = Depends(get_session), employee_id: int
):
    return time_entry_dal.get_entries_by_model(session, db_models.Employee, employee_id)


@router.get("/job/{job_id}", response_model=List[TimeEntriesRead])
def show_time_entries_by_job(*, session: Session = Depends(get_session), job_id: int):
    return time_entry_dal.get_entries_by_model(session, db_models.Job, job_id)


@router.post(
    "/employee/{employee_id}",
    response_model=TimeEntriesRead,
    status_code=status.HTTP_201_CREATED,
)
def time_entry_create(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    time_entry: TimeEntriesCreate
):
    time_entry = TimeEntries.from_orm(time_entry)
    employee = session.get(Employee, employee_id)
    employee.time_entries.append(time_entry)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return time_entry


@router.patch("/{id}", response_model=TimeEntriesRead)
def updated_time_entry(
    *, session: Session = Depends(get_session), id: int, time_entry: TimeEntriesUpdate
):
    db_time_entry = session.get(TimeEntries, id)
    if not db_time_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="time entry not found"
        )
    time_entry_data = time_entry.dict(exclude_unset=True)
    for k, v in time_entry_data.items():
        setattr(db_time_entry, k, v)

    session.add(db_time_entry)
    session.commit()
    session.refresh(db_time_entry)
    return db_time_entry


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def time_entry_deleted(*, session: Session = Depends(get_session), id: int):
    db_time_entry = session.get(TimeEntries, id)
    if not db_time_entry:
        raise HTTPException(status_code=404, detail="entry not found")
    session.delete(db_time_entry)
    session.commit()
    return {"deleted": "accepted"}
