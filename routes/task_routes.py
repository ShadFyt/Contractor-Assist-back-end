from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models.db import get_session
from models.task_models import TaskCreate, TaskRead, TaskUpdate
from models.db_models import Job, Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/{job_id}", response_model=List[TaskRead])
def get_task_by_job(*, session: Session = Depends(get_session), job_id: int):
    job = session.get(Job, job_id)
    return job.tasks


@router.post("/{job_id}", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def task_created(
    *, session: Session = Depends(get_session), job_id: int, task: TaskCreate
):
    new_task = Task.from_orm(task)
    job = session.get(Job, job_id)
    job.tasks.append(new_task)
    session.add(job)
    session.commit()
    session.refresh(job)

    return new_task


@router.patch(
    "/{task_id}", response_model=TaskRead, status_code=status.HTTP_202_ACCEPTED
)
def update_task(
    *, session: Session = Depends(get_session), task_id: int, updatedTask: TaskUpdate
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    task_data = updatedTask.dict(exclude_unset=True)
    for k, v in task_data.items():
        setattr(task, k, v)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def task_delete(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="task not found"
        )
    session.delete(task)
    session.commit()
