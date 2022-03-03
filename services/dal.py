from fastapi import status, HTTPException
from typing import List
from datetime import datetime, date, timedelta

from sqlmodel import Session, select

from models.db_models import Employee, Task, Job, TimeEntries


class BaseDal:
    """An interface to handle operations to the database. 'Data access layer'"""

    def __init__(self, model, name: str) -> None:
        self.model = model
        self.name = name

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
        if db_item := session.get(self.model, id):
            return db_item
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
        )

    def create(self, session: Session, post):
        new_db_item = self.model.from_orm(post)
        return self._handle_session(session, new_db_item)

    def modify(self, session: Session, id: int, post):
        # gets item from database & checks if item not in database return exception
        if not (db_item := session.get(self.model, id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{self.name} not found"
            )
        # gets the client data and converts it from json into a python dict
        item_data = post.dict(exclude_unset=True)
        for k, v in item_data.items():
            setattr(db_item, k, v)
        return self._handle_session(session, db_item)

    def destroy(self, session, id):
        if not (item := session.get(self.model, id)):
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
    def __init__(self, model: Employee = Employee, name: str = "employee") -> None:
        super().__init__(model, name)
        self.model = model
        self.name = name

    def get_one_by_name(self, session: Session, name: str):
        return session.exec(
            select(self.model).where(self.model.first_name == name)
        ).one_or_none()


class ClientDal(BaseDal):
    ...


class JobDal(BaseDal):
    ...


class TaskDal(BaseDal):
    def __init__(self, model: Task = Task, name: str = "task") -> None:
        super().__init__(model, name)

    def create(self, session: Session, post, job_id):
        new_task = self.model.from_orm(post)
        job = session.get(Job, job_id)
        job.tasks.append(new_task)

        super()._handle_session(session, db_item=job)
        return new_task

    def find_all_by_job(self, session: Session, job_id: int) -> List[Task]:
        job = session.get(Job, job_id)
        return job.tasks


class TimeEntry(BaseDal):
    def __init__(
        self, model: TimeEntries = TimeEntries, name: str = "time entries"
    ) -> TimeEntries:
        super().__init__(model, name)

    def get_entries_by_model(
        self, session: Session, _model, _id: int
    ) -> List[TimeEntries]:
        db_model = session.get(_model, _id)
        return db_model.time_entries

    def get_entries_by_date_range(self, session: Session):
        date_range = self._get_date_range()
        print(date_range)
        stmt = (
            select(TimeEntries)
            .where(TimeEntries.date >= date_range[0])
            .where(TimeEntries.date <= date_range[-1])
        )
        results = session.exec(stmt).all()
        for item in results:
            print(item)

        return results

    def create(self, session: Session, post, employee_id):
        new_time_entry = self.model.from_orm(post)
        if employee := session.get(Employee, employee_id):
            employee.time_entries.append(new_time_entry)
            super()._handle_session(session, employee)
            return new_time_entry
        print("no record of employee found")

    def _get_date_range(self):
        number_of_days: int = 7
        start_date = date(2022, 2, 11)
        return [
            (start_date + timedelta(days=day)).isoformat()
            for day in range(number_of_days)
        ]
