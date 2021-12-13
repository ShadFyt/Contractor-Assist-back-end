import fastapi
import uvicorn

from models.db import create_db_and_tables, engine
from models.jobs_models import Job, Employee
from routes import employees_routes, job_routes


app = fastapi.FastAPI()
app.include_router(employees_routes.router)
app.include_router(job_routes.router)


def main():
    create_db_and_tables()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
