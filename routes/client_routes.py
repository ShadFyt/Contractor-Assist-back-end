from fastapi import APIRouter, status, Depends
from typing import List

from sqlmodel import Session
from internal.admin import get_current_active_user

from models.client_models import (
    ClientRead,
    ClientCreate,
    ClientUpdate,
    ClientReadWithJob,
    Client,
)
from models.db import get_session

from services.dal import ClientDal


router = APIRouter(prefix="/clients", tags=["clients"])

client_dal = ClientDal(Client, "client")


@router.get(
    "/",
    response_model=List[ClientReadWithJob],
    dependencies=[Depends(get_current_active_user)],
)
async def show_all_clients(session: Session = Depends(get_session)):
    return client_dal.get_all(session)


@router.get("/{client_id}", response_model=ClientRead)
def get_client_by_id(*, session: Session = Depends(get_session), client_id: int):
    return client_dal.get_one_by_id(session, client_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClientRead)
def create_client(*, session: Session = Depends(get_session), client: ClientCreate):
    return client_dal.create(session, client)


@router.patch(
    "/{client_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ClientRead
)
def update_client(
    *, session: Session = Depends(get_session), client_id: int, client: ClientUpdate
):
    return client_dal.modify(session, client_id, client)


@router.delete("/{client_id}")
def delete_client(*, session: Session = Depends(get_session), client_id: int):
    client_dal.destroy(session, client_id)
    return {status.HTTP_204_NO_CONTENT: True}
