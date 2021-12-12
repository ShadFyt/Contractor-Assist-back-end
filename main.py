import fastapi
import uvicorn

from models.db import create_db_and_tables, engine
from models import employees
from routes import employees_routes


app = fastapi.FastAPI()
app.include_router(employees_routes.router)


def main():
    create_db_and_tables()
    uvicorn.run(app)


if __name__ == "__main__":
    main()
