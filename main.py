from fastapi import FastAPI
from routes import recipes_routes

app = FastAPI()
app.include_router(recipes_routes.router)
