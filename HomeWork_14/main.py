# # main.py
# import cloudinary
# import crud, mail_service
# from database import models
# import auth, users
# import jwt
#
# from cloudinary.uploader import upload
# from datetime import timedelta
# from contextlib import asynccontextmanager
# from anyio.streams import file
# from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy import text
# from sqlalchemy.orm import Session
#
# from database.db import get_db, Base, engine # для тестування
# # from database import engine, get_db # для роботи
# from models import User as UserModel
# from schemas import User, UserCreate, ContactCreate, Contact, Token, UserUpdateSchema, UserResponse
# from rate_limiter import RateLimiter
# from config import settings
# from auth import get_current_user
# import auth, users
#
# # Функція для запуску та зупинки застосунку
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """
#     Handle startup and shutdown events for the application.
#     """
#     # Створюємо таблиці в базі даних при старті.
#     print("Creating database tables...")
#     try:
#         models.Base.metadata.create_all(bind=engine)
#         print("Database tables created successfully!")
#     except Exception as e:
#         print(f"Error creating database tables: {e}")
#         # Застосунок може не працювати без таблиць, тому можна завершити його
#         raise RuntimeError("Failed to connect to database or create tables.")
#     yield
#     # Логіка для вимкнення, якщо потрібно
#
# # Ініціалізація FastAPI
# app = FastAPI(
#     title="Contacts API",
#     description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
#     version="1.0.0",
#     lifespan=lifespan
# )
#
# # Налаштування Cloudinary
# cloudinary.config(
#     cloud_name=settings.CLOUDINARY_CLOUD_NAME,
#     api_key=settings.CLOUDINARY_API_KEY,
#     api_secret=settings.CLOUDINARY_API_SECRET
# )
#
# # Налаштування CORS
# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     settings.FRONTEND_URL,
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# # ---
# ## Ендпоїнти загальні та для користувачів
#
# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Contacts API!"}
#
# @app.get("/api/healthchecker")
# def healthchecker(db: Session = Depends(get_db)):
#     try:
#         # Перевіряємо з'єднання з базою даних
#         result = db.execute(text("SELECT 1")).scalar()
#         if result == 1:
#             return {"message": "Database is healthy!"}
#         else:
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not healthy")
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to the database")
#
#
# # @app.patch("/users/avatar", response_model=User)
# # @app.patch("/users/avatar", response_model=UserSchema)
# @app.patch("/users/avatar", response_model=UserResponse)
# async def update_avatar(
#         body: UserUpdateSchema,
#         current_user: UserModel = Depends(get_current_user),
#         db: Session = Depends(get_db)):
# # async def update_avatar(
# #     file: UploadFile = File(...),
# #     current_user: User = Depends(auth.get_current_user),
# #     db: Session = Depends(get_db)
# # ):
#     """
#     Update the user's avatar by uploading a file to Cloudinary.
#     """
#     try:
#         # Uploading the file to Cloudinary
#         result = cloudinary.uploader.upload(file.file, folder="avatars")
#         avatar_url = result.get("secure_url")
#         current_user.avatar = avatar_url
#         db.commit()
#         db.refresh(current_user)
#         return current_user
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
#
# @app.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
# async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
#     """
#     Register a new user and send a verification email.
#     """
#     db_user = users.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
#
#     new_user = users.create_user(db=db, user=user)
#
#     background_tasks.add_task(mail_service.send_email_verification, new_user.email, new_user.email, settings.FRONTEND_URL)
#
#     return new_user
#
# @app.get("/verify-email/{token}")
# def verify_email(token: str, db: Session = Depends(get_db)):
#     """
#     Verify user's email using a JWT token.
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[auth.ALGORITHM])
#         email = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         user = db.query(User).filter(User.email == email).first()
#         if not user:
#             raise credentials_exception
#         if user.is_verified:
#             return {"message": "Email already verified"}
#
#         user.is_verified = True
#         db.commit()
#         return {"message": "Email successfully verified"}
#     except jwt.JWTError:
#         raise credentials_exception
#
# @app.post("/token", response_model=Token)
# def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     """
#     Log in a user and get access and refresh tokens.
#     """
#     user = users.get_user_by_email(db, email=form_data.username)
#     if not user or not auth.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth.create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     refresh_token = auth.create_refresh_token(
#         data={"sub": user.email}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
#     )
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
#
# # ---
# ## Ендпоїнти контактів
# @app.post("/contacts/", response_model=Contact, status_code=status.HTTP_201_CREATED,
#           dependencies=[Depends(RateLimiter(times=2, minutes=5))])
# def create_new_contact(
#     contact: ContactCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(auth.get_current_user)
# ):
#     """
#     Create a new contact for the current user.
#     """
#     return crud.create_contact_for_user(db=db, contact=contact, user_id=current_user.id)
#
# @app.get("/contacts/", response_model=list[Contact])
# def read_contacts(
#     skip: int = 0,
#     limit: int = 100,
#     current_user: User = Depends(auth.get_current_user),
#     db: Session = Depends(get_db)
# ):
#     """
#     Retrieve a list of contacts for the current user.
#     """
#     return crud.get_user_contacts(db, user_id=current_user.id, skip=skip, limit=limit)
#
# @app.get("/contacts/{contact_id}", response_model=Contact)
# def read_contact(
#     contact_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(auth.get_current_user)
# ):
#     """
#     Retrieve a specific contact by ID for the current user.
#     """
#     contact = crud.get_contact_by_id_for_user(db, contact_id, current_user.id)
#     if not contact:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
#     return contact
#
# @app.put("/contacts/{contact_id}", response_model=Contact)
# def update_contact(
#     contact_id: int,
#     contact_update: ContactCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(auth.get_current_user)
# ):
#     """
#     Update an existing contact for the current user.
#     """
#     contact = crud.update_contact_for_user(db, contact_id, current_user.id, contact_update)
#     if not contact:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or does not belong to the user")
#     return contact
#
# @app.delete("/contacts/{contact_id}", response_model=Contact)
# def delete_contact(
#     contact_id: int,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(auth.get_current_user)
# ):
#     """
#     Delete a contact for the current user.
#     """
#     contact = crud.delete_contact_for_user(db, contact_id, current_user.id)
#     if not contact:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or does not belong to the user")
#     return contact

# main.py

# --- Верхній рівень: імпорти, які не спричиняють циклічних залежностей ---
import cloudinary
import crud, mail_service
import auth, users
import jwt

from cloudinary.uploader import upload
from datetime import timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session
# from models import User as UserModel
from database.db import get_db, engine
from schemas import User, UserCreate, ContactCreate, Contact, Token, UserUpdateSchema, UserResponse
from rate_limiter import RateLimiter
from config import settings
from database import models # <-- Залишаємо цей імпорт
from database.models import User as UserModel
from typing import List, Optional


# ---
# Функція для запуску та зупинки застосунку
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events for the application.
    """
    print("Creating database tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise RuntimeError("Failed to connect to database or create tables.")
    yield

# Ініціалізація FastAPI
app = FastAPI(
    title="Contacts API",
    description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan
)

# Налаштування Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# Налаштування CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---
## Ендпоїнти загальні та для користувачів

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contacts API!"}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        if result == 1:
            return {"message": "Database is healthy!"}
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database is not healthy")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connecting to the database")

# Виправлення для оновлення аватара
@app.patch("/users/avatar", response_model=UserResponse)
async def update_avatar(
        file: UploadFile = File(...),
        current_user: UserModel = Depends(auth.get_current_user),
        db: Session = Depends(get_db)):
    try:
        result = upload(file.file, folder="avatars")
        avatar_url = result.get("secure_url")
        current_user.avatar = avatar_url
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = users.create_user(db=db, user=user)

    background_tasks.add_task(mail_service.send_email_verification, new_user.email, new_user.email, settings.FRONTEND_URL)

    return new_user

@app.get("/verify-email/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise credentials_exception
        if user.is_verified:
            return {"message": "Email already verified"}

        user.is_verified = True
        db.commit()
        return {"message": "Email successfully verified"}
    except jwt.JWTError:
        raise credentials_exception

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = users.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = auth.create_refresh_token(
        data={"sub": user.email}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ---
## Ендпоїнти контактів
@app.post("/contacts/", response_model=Contact, status_code=status.HTTP_201_CREATED,
          dependencies=[Depends(RateLimiter(times=2, minutes=5))])
def create_new_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth.get_current_user)
):
    return crud.create_contact_for_user(db=db, contact=contact, user=current_user)

@app.get("/contacts/", response_model=list[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_contacts(db, user=current_user, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth.get_current_user)
):
    contact = crud.get_contact_by_id_for_user(db, contact_id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact_update: ContactCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth.get_current_user)
):
    contact = crud.update_contact(db, contact_id, contact_update, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or does not belong to the user")
    return contact

@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(auth.get_current_user)
):
    contact = crud.delete_contact(db, contact_id, current_user)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found or does not belong to the user")
    return contact

# --- Додаткові ендпоїнти ---

@app.get("/contacts/search/", response_model=List[Contact])
def search_contacts(
    query: Optional[str] = None,
    current_user: UserModel = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.search_contacts(db, query, current_user)

@app.get("/contacts/birthdays/", response_model=List[Contact])
def get_upcoming_birthdays(
    current_user: UserModel = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_upcoming_birthdays(db, current_user)