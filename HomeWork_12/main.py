# from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import List, Optional
#
# from database import engine, Base, get_db
# from models import Contact
# from schemas import Contact as ContactSchema, ContactCreate, ContactUpdate
# import crud
#
# app = FastAPI(
#     title="Contacts API",
#     description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
#     version="1.0.0",
# )
#
# Base.metadata.create_all(bind=engine)
#
# @app.post("/contacts/", response_model=ContactSchema)
# def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
#     db_contact = crud.get_contact_by_email(db, email=contact.email)
#     if db_contact:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_contact(db=db, contact=contact)
#
# @app.get("/contacts/", response_model=List[ContactSchema])
# def read_contacts(
#     skip: int = 0,
#     limit: int = 100,
#     query: Optional[str] = Query(None, min_length=1, description="Search by first name, last name, or email"),
#     db: Session = Depends(get_db)
# ):
#     if query:
#         contacts = crud.search_contacts(db, query)
#     else:
#         contacts = crud.get_contacts(db, skip=skip, limit=limit)
#     return contacts
#
# @app.get("/contacts/{contact_id}", response_model=ContactSchema)
# def read_contact(contact_id: int, db: Session = Depends(get_db)):
#     db_contact = crud.get_contact_by_id(db, contact_id=contact_id)
#     if db_contact is None:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return db_contact
#
# @app.put("/contacts/{contact_id}", response_model=ContactSchema)
# def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
#     db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
#     if db_contact is None:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return db_contact
#
# @app.delete("/contacts/{contact_id}", response_model=ContactSchema)
# def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
#     db_contact = crud.delete_contact(db, contact_id=contact_id)
#     if db_contact is None:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return db_contact
#
# @app.get("/contacts/birthdays/", response_model=List[ContactSchema])
# def upcoming_birthdays(db: Session = Depends(get_db)):
#     contacts = crud.get_upcoming_birthdays(db)
#     return contacts

from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, Base, get_db
from schemas import Contact as ContactSchema, ContactCreate, ContactUpdate, User as UserSchema, UserCreate, Token
import crud, users, auth
from models import User, Contact

app = FastAPI(
    title="Contacts API",
    description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)

# Ендпоїнт для реєстрації
@app.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return users.create_user(db=db, user=user)

# Ендпоїнт для входу та отримання токенів
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.email}, expires_delta=timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Оновлені ендпоїнти для контактів з авторизацією
@app.post("/contacts/", response_model=ContactSchema, status_code=status.HTTP_201_CREATED)
def create_new_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    # Користувач тепер доступний через `current_user`
    return crud.create_contact_for_user(db=db, contact=contact, user_id=current_user.id)

@app.get("/contacts/", response_model=List[ContactSchema])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Тепер отримуємо лише контакти поточного користувача
    return crud.get_user_contacts(db, user_id=current_user.id, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    contact = crud.get_contact_by_id_for_user(db, contact_id, current_user.id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

