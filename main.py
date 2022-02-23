from fastapi import FastAPI
from routes import recipes_routes
import uvicorn

app = FastAPI()
app.include_router(recipes_routes.router)


def main():
    uvicorn.run(app, port=8000, host="127.0.0.1")


if __name__ == "__main__":
    main()
