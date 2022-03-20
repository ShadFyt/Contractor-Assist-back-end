from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from typing import List
from models.db import get_session
from models.task_models import TaskCreate, TaskRead, TaskUpdate
from internal import admin

from services.dal import TaskDal

router = APIRouter(prefix="/tasks", tags=["tasks"])

taskDal = TaskDal()


@router.get(
    "/{job_id}",
    response_model=List[TaskRead],
    dependencies=[Depends(admin.get_current_active_user)],
)
def get_tasks_by_job(*, session: Session = Depends(get_session), job_id: int):
    return taskDal.find_all_by_job(session, job_id)


@router.post("/{job_id}", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def task_created(
    *, session: Session = Depends(get_session), job_id: int, task: TaskCreate
):
    return taskDal.create(session, task, job_id)


@router.patch(
    "/{task_id}", response_model=TaskRead, status_code=status.HTTP_202_ACCEPTED
)
def update_task(
    *, session: Session = Depends(get_session), task_id: int, updatedTask: TaskUpdate
):
    return taskDal.modify(session, task_id, updatedTask)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def task_delete(*, session: Session = Depends(get_session), task_id: int):
    taskDal.destroy(session, task_id)
