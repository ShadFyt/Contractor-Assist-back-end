from fastapi import status, HTTPException
from typing import List

from sqlmodel import Session, select

from models import db_models


class BaseDal:
    def __init__(self, model, name) -> None:
        self.model = model
        self.name: str = name

    def get_all(self, session: Session) -> List:
        return session.exec(select(self.model)).all()

    def get_one_by_id(self, session: Session, id: int):
        db_item = session.get(self.model, id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        return db_item

    def create(self, session: Session, post):
        new_db_item = self.model.from_orm(post)
        return self._handle_session(session, new_db_item)

    def modify(self, session: Session, id: int, post):
        db_item = session.get(self.model, id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        item_data = post.dict(exclude_unset=True)
        for k, v in item_data.items():
            setattr(db_item, k, v)
        return self._handle_session(session, db_item)

    def destroy(self, session, id):
        item = session.get(self.model, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        session.delete(item)
        session.commit()

    def _handle_session(self, session, db_item):
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


class EmployeeDal(BaseDal):
    def __init__(self, model: db_models.Employee, name: str) -> None:
        self.model = model
        super().__init__(model, name)

    def get_one_by_name(self, session: Session, name: str):
        return session.exec(
            select(self.model).where(self.model.first_name == name)
        ).one_or_none()


class ClientDal(BaseDal):
    ...


class JobDal(BaseDal):
    ...


class TaskDal(BaseDal):
    ...


class TimeEntry(BaseDal):
    def __init__(self, model: db_models.TimeEntries, name: str) -> None:
        self.model = model
        super().__init__(model, name)

    def get_entries_by_model(self, session: Session, _model, _id: int):
        db_model = session.get(_model, _id)
        return db_model.time_entries
