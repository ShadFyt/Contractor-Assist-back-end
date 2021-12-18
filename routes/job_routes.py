from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models.db import get_session

from models.jobs_models import Job, JobCreate, JobRead, JobReadWithTimes, JobUpdate


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=List[JobRead], status_code=status.HTTP_202_ACCEPTED)
def get_all_jobs(session: Session = Depends(get_session)):
    return session.exec(select(Job)).all()


@router.get("/{job_id}", response_model=JobReadWithTimes)
def get_single_job(*, session: Session = Depends(get_session), job_id: int):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found"
        )
    return job


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(*, session: Session = Depends(get_session), job: JobCreate):
    db_job = Job.from_orm(job)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.patch("/{job_id}", response_model=JobRead, status_code=status.HTTP_202_ACCEPTED)
def update_job(*, session: Session = Depends(get_session), job_id: int, job: JobUpdate):
    db_job = session.get(Job, job_id)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="job not found"
        )

    job_data = job.dict(exclude_unset=True)
    for k, v in job_data.items():
        setattr(db_job, k, v)

    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def job_deleted(*, session: Session = Depends(get_session), job_id: int):
    db_job = session.get(Job, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="job not found")

    session.delete(db_job)
    session.commit
    return {"delete": "accepted"}
