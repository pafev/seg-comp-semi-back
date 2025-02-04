from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.users import users_interfaces, users_repository


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=users_interfaces.User)
def create_user(user: users_interfaces.UserCreate, db: Session = Depends(get_db)):
    if users_repository.get_user_by_name(db, user_name=user.name):
        raise HTTPException(status_code=400, detail="Usuarios ja existe")
    return users_repository.create_user(db=db, user_create=user)


@router.get("/user_id/{user_id}", response_model=users_interfaces.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_repository.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return user


@router.post("/sign-in", response_model=users_interfaces.User)
def sign_in(user_sign_in: users_interfaces.UserSignIn, db: Session = Depends(get_db)):
    user = users_repository.sing_in(db=db, user_sign_in=user_sign_in)
    if not user:
        raise HTTPException(status_code=401, detail="Não foi possivel autenticar")
    return user
