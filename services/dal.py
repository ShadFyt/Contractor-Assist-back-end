from fastapi import status, HTTPException
from typing import List
from datetime import datetime, date, timedelta

from sqlmodel import Session, select

from models.db_models import Employee, Task, TimeEntries
from models.jobs_models import Job


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

    def get_entries_by_date_range(self, session: Session, week_of):
        date_range = self._get_date_range(week_of)
        print(date_range)
        stmt = (
            select(TimeEntries)
            .where(TimeEntries.date >= date_range[0])
            .where(TimeEntries.date <= date_range[-1])
        )
        return session.exec(stmt).all()

    def create(self, session: Session, post, employee_id):
        new_time_entry = self.model.from_orm(post)
        if employee := session.get(Employee, employee_id):
            employee.time_entries.append(new_time_entry)
            super()._handle_session(session, employee)
            return new_time_entry
        print("no record of employee found")

    def _get_date_range(self, start_date: date):
        """takes a date, checks if date is a Monday if not Monday change date to monday.
            ex: _get_date_range("2022-02-10")

        Args:
            start_date (date): a date object in isoformat
            ex: "YYY-MM=DD"

        Returns:
            List[date]: List of 7 dates starting from a Monday
            ex: ['2022-02-07', '2022-02-08', '2022-02-09', '2022-02-10', '2022-02-11', '2022-02-12', '2022-02-13']
        """
        number_of_days: int = 7
        if start_date.weekday() > 0:
            start_date -= timedelta(days=start_date.weekday())
        return [
            (start_date + timedelta(days=day)).isoformat()
            for day in range(number_of_days)
        ]
