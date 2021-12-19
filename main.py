import fastapi
import uvicorn

from models.db import create_db_and_tables
from models.db_models import Job, Employee, TimeEntries, Task
from routes import employees_routes, job_routes, time_entries_routes, task_routes


app = fastapi.FastAPI()
app.include_router(employees_routes.router)
app.include_router(job_routes.router)
app.include_router(time_entries_routes.router)
app.include_router(task_routes.router)


def main():
    create_db_and_tables()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
