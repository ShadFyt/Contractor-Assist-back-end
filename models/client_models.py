from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


from .jobs_models import JobRead


from humps import camelize


if TYPE_CHECKING:
    from .jobs_models import Job


def to_camel(string):
    return camelize(string)


class ClientBase(SQLModel):
    first_name: str = Field(index=True)
    last_name: str
    phone_number: str
    email: str

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class Client(ClientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    jobs: List["Job"] = Relationship(back_populates="client")


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
    id: int
    jobs: List[JobRead] = []
