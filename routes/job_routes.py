from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from typing import List
from models.db import get_session

from models.jobs_models import JobCreate, JobRead, JobReadWithTasksAndTimes, JobUpdate
from models.db_models import Job

from services.dal import JobDal

router = APIRouter(prefix="/jobs", tags=["jobs"])

jobDal = JobDal(Job, "job")


@router.get(
    "/",
    response_model=List[JobReadWithTasksAndTimes],
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_all_jobs(session: Session = Depends(get_session)):
    return jobDal.get_all(session)


@router.get("/{job_id}", response_model=JobReadWithTasksAndTimes)
def get_single_job(*, session: Session = Depends(get_session), job_id: int):
    return jobDal.get_one_by_id(session, job_id)


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(*, session: Session = Depends(get_session), job: JobCreate):
    return jobDal.create(session, job)


@router.patch("/{job_id}", response_model=JobRead, status_code=status.HTTP_202_ACCEPTED)
def update_job(*, session: Session = Depends(get_session), job_id: int, job: JobUpdate):
    return jobDal.modify(session, job_id, job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def job_deleted(*, session: Session = Depends(get_session), job_id: int):
    jobDal.destroy(session, job_id)
    return {"delete": "accepted"}
