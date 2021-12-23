from typing import List, Optional

from .base_models import ClientBase
from .jobs_models import JobRead


class ClientCreate(ClientBase):
    pass

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": 8889999999,
                "email": "fake@hotmail.com",
            }
        }


class ClientRead(ClientBase):
    id: int


class ClientUpdate(ClientBase):
    pass


class ClientReadWithJob(ClientBase):
    jobs: List[JobRead] = []
