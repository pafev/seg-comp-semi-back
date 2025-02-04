from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    password: str


class UserSignIn(BaseModel):
    name: str
    password: str


class User(BaseModel):
    id: int
    name: str
    password: str

    class Config:
        from_attributes = True
