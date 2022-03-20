from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from humps import camelize


def to_camel(string):
    return camelize(string)


class OrganizationBase(SQLModel):
    name: str
