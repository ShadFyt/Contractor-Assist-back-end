from fastapi import status, HTTPException
from typing import List

from sqlmodel import Session, select

from models import db_models


class BaseDal:
    """An interface to handle operations to the database. 'Data access layer'"""

    def __init__(self, model, name) -> None:
        self.model = model
        self.name: str = name

    def get_all(self, session: Session) -> List:
        """returns list of all entries of self.model from database

        Args:
            session (Session): opens a connection to the database,
            self.model (Table):  represent a table in the database

        Returns:
            List: returns all columns of self.table
        """
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
        """Opens connection to the database

        Args:
            session (Session): establishes all conversations with the database
            db_item (Object): An object that represents a table in the SQL database

        Returns:
            db_item: returns a unique record from the database
        """
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
    pass


class TaskDal(BaseDal):
    def __init__(self, model: db_models.Task, name: str) -> None:
        self.model = model
        super().__init__(model, name)

    def create(self, session: Session, post, job_id):
        new_task = self.model.from_orm(post)
        job = session.get(db_models.Job, job_id)
        job.tasks.append(new_task)

        self._handle_session(session, db_item=job)
        return new_task

    def find_all_by_job(self, session: Session, job_id: int) -> List[db_models.Task]:
        job = session.get(db_models.Job, job_id)
        return job.tasks

    def _handle_session(self, session, db_item):
        return super()._handle_session(session, db_item)


class TimeEntry(BaseDal):
    def __init__(self, model: db_models.TimeEntries, name: str) -> None:
        self.model = model
        super().__init__(model, name)

    def get_entries_by_model(
        self, session: Session, _model, _id: int
    ) -> List[db_models.TimeEntries]:
        db_model = session.get(_model, _id)
        return db_model.time_entries

    def create(self, session: Session, post, employee_id):
        new_time_entry = self.model.from_orm(post)
        employee = session.get(db_models.Employee, employee_id)
        if employee:
            employee.time_entries.append(new_time_entry)
        else:
            print("no record of employee found")
        self._handle_session(session, employee)
        return new_time_entry

    def _handle_session(self, session, db_item):
        return super()._handle_session(session, db_item)
