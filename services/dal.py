from abc import ABC, abstractmethod
from fastapi import status, HTTPException
from typing import List

from sqlmodel import Session, select


class BaseDal:
    def __init__(self, model, name) -> None:
        self.model = model
        self.name: str = name

    def get_all(self, session: Session) -> List:
        print()
        return session.exec(select(self.model)).all()

    def get_one_by_id(self, session: Session, id: int):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        return item

    def create(self, session: Session, post):
        new_db_item = self.model.from_orm(post)
        session.add(new_db_item)
        session.commit()
        session.refresh(new_db_item)
        return new_db_item

    def modify(self, session: Session, id: int, post):
        db_item = session.get(self.model, id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        item_data = post.dict(exclude_unset=True)
        for k, v in item_data.items():
            setattr(db_item, k, v)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

    def destroy(self, session, id):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        session.delete(item)
        session.commit()
