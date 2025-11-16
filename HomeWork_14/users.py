# users.py
from sqlalchemy.orm import Session
# from models import User
from sqlalchemy.orm import Session
from database.models import User  # <-- Змінено тут
from schemas import UserCreate
from passlib.context import CryptContext
from typing import Optional

from schemas import UserCreate
from auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
