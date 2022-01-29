from fastapi import APIRouter, status, Depends, HTTPException
from typing import List

from sqlmodel import Session, select

from models.client_models import (
    ClientRead,
    ClientCreate,
    ClientUpdate,
    ClientReadWithJob,
)
from models.db_models import Client
from models.db import get_session

from services import client_utils


router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[ClientReadWithJob])
async def show_all_clients(session: Session = Depends(get_session)):
    return client_utils.get_all(session)


@router.get("/{client_id}", response_model=ClientRead)
def get_client_by_id(*, session: Session = Depends(get_session), client_id: int):
    return client_utils.get_one_by_id(session, client_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClientRead)
def create_client(*, session: Session = Depends(get_session), client: ClientCreate):
    return client_utils.create(session, client)


@router.patch(
    "/{client_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ClientRead
)
def update_client(
    *, session: Session = Depends(get_session), client_id: int, client: ClientUpdate
):
    return client_utils.modify(session, client_id, client)


@router.delete("/{client_id}")
def delete_client(*, session: Session = Depends(get_session), client_id: int):
    client_utils.destroy(session, client_id)
    return {status.HTTP_204_NO_CONTENT: True}
