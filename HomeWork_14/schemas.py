# schemas.py
from pydantic import BaseModel, Field, EmailStr
from datetime import date, datetime
from typing import Optional


class UserUpdateSchema(BaseModel):
    # Ви можете додати будь-які поля, які хочете дозволити оновлювати.
    # Наприклад, тільки 'avatar'.
    avatar: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str | None = None

    class Config:
        from_attributes = True  # Це важливо для Pydantic V2.

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str | None = None  # Залежно від того, які поля у вас є

    class Config:
        from_attributes = True  # Pydantic V2: дозволяє моделі читати дані з атрибутів
        # orm_mode = True       # Pydantic V1: робить те ж саме

class ContactBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None

class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None

