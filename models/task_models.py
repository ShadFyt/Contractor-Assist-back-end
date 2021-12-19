from .base_models import TaskBase


class TaskRead(TaskBase):
    id: int


class TaskCreate(TaskBase):
    pass

    class Config:
        schema_extra = {"example": {"task": "Some task", "is_complete": False}}


class TaskUpdate(TaskBase):
    pass


class TaskDelete(TaskBase):
    pass
