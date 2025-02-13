from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.db import engine
from app.files import files_routes
from app.users import users_routes


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://seg-comp-semi-front-production.up.railway.app",
    "https://seg-comp-semi-front-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return "Hello World"


app.include_router(users_routes.router)
app.include_router(files_routes.router)
