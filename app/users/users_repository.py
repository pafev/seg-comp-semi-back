from sqlalchemy.orm import Session

from app.models import User
from app.users.users_interfaces import UserCreate, UserSignIn


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.name == user_name).first()


def create_user(db: Session, user_create: UserCreate):
    db_user_create = User(name=user_create.name, password=user_create.password)
    db.add(db_user_create)
    db.commit()
    db.refresh(db_user_create)
    return db_user_create


def sing_in(db: Session, user_sign_in: UserSignIn):
    return (
        db.query(User)
        .filter(User.name == user_sign_in.name, User.password == user_sign_in.password)
        .first()
    )
