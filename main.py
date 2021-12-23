import fastapi
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from models.db import create_db_and_tables
from models.db_models import Job, Employee, TimeEntries, Task, Client
from routes import (
    employees_routes,
    job_routes,
    time_entries_routes,
    task_routes,
    client_routes,
)


app = fastapi.FastAPI()
app.include_router(employees_routes.router)
app.include_router(job_routes.router)
app.include_router(time_entries_routes.router)
app.include_router(task_routes.router)
app.include_router(client_routes.router)

origins = ["https://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    create_db_and_tables()
    uvicorn.run(app, port=8000, host="127.0.0.1")


if __name__ == "__main__":
    main()
