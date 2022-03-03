from fastapi import APIRouter, status, Depends
from typing import List
from datetime import date


from sqlmodel import Session
from models import db_models

from models.time_entry_models import (
    TimeEntriesRead,
    TimeEntriesCreate,
    TimeEntriesUpdate,
)
from models.db_models import TimeEntries

from models.db import get_session
from services import dal

router = APIRouter(prefix="/time_sheet", tags=["Time Sheet"])

time_entry_dal = dal.TimeEntry(TimeEntries, "time entry")


@router.get("/{id}", response_model=TimeEntriesRead)
def get_time_entry_by_id(*, session: Session = Depends(get_session), id: int):
    return time_entry_dal.get_one_by_id(session, id)


@router.get("/week/{week_of}", response_model=List[TimeEntriesRead])
def get_time_entries_by_week(*, session: Session = Depends(get_session), week_of):
    return time_entry_dal.get_entries_by_date_range(session)


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
    return time_entry_dal.create(session, time_entry, employee_id)


@router.patch("/{id}", response_model=TimeEntriesRead)
def updated_time_entry(
    *, session: Session = Depends(get_session), id: int, time_entry: TimeEntriesUpdate
):
    return time_entry_dal.modify(session, id, time_entry)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def time_entry_deleted(*, session: Session = Depends(get_session), id: int):
    time_entry_dal.destroy(session, id)
    return {"deleted": "accepted"}
