from fastapi import FastAPI

from app import models
from app.db import engine
from app.files import files_routes
from app.users import users_routes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def hello_world():
    return "Hello World"


app.include_router(users_routes.router)
app.include_router(files_routes.router)
