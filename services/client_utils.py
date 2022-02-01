from fastapi import status, HTTPException

from sqlmodel import select
from models import db_models


def get_all(session):
    print("getting clients")
    return session.exec(select(db_models.Client)).all()


def get_one_by_id(session, client_id):
    client = session.get(db_models.Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )
    return client


def create(session, client):
    new_client = db_models.Client.from_orm(client)
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    return new_client


def modify(session, client_id, client):
    db_client = session.get(db_models.Client, client_id)
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


def destroy(session, client_id):
    client = session.get(db_models.Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="client not found"
        )
    session.delete(client)
    session.commit()
