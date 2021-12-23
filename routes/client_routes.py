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


router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/", response_model=List[ClientReadWithJob])
async def show_all_clients(session: Session = Depends(get_session)):
    return session.exec(select(Client)).all()


@router.get("/{client_id}", response_model=ClientRead)
def get_client_by_id(*, session: Session = Depends(get_session), client_id: int):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClientRead)
def create_client(*, session: Session = Depends(get_session), client: ClientCreate):
    new_client = Client.from_orm(client)
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return new_client


@router.patch(
    "/{client_id}", status_code=status.HTTP_202_ACCEPTED, response_model=ClientRead
)
def update_client(
    *, session: Session = Depends(get_session), client_id: int, client: ClientUpdate
):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="client not found"
        )
    client_data = client.dict(exclude_unset=True)
    for k, v in client_data.items():
        setattr(db_client, k, v)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client


@router.delete("/{client_id}")
def delete_client(*, session: Session = Depends(get_session), client_id: int):

    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Clients not found"
        )

    session.delete(client)
    session.commit()
    return {status.HTTP_204_NO_CONTENT: True}
