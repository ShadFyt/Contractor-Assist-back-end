# from datetime import datetime
# from sqlmodel import SQLModel, Field
# from typing import Optional


# class JobBase(SQLModel):
#     job_name: Optional[str]
#     is_complete: bool = False
#     summary: Optional[str]
#     start_date: Optional[str]
#     finish_date: Optional[str]
#     job_type: Optional[str]


# class EmployeeBase(SQLModel):
#     first_name: str
#     last_name: str
#     birth_date: str
#     pay_rate: float


# class TimeEntriesBase(SQLModel):
#     date: str
#     clock_in: datetime
#     clock_out: datetime
#     hours: Optional[int]

#     job_id: Optional[int] = Field(default=None, foreign_key="job.id")
